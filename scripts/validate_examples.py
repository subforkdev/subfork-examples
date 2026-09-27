#!/usr/bin/env python3
"""Validate portable Subfork example documents without application dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
GRAPH_ROOT = ROOT / "graphs"
CATALOG_MAX_BYTES = 5 * 1024 * 1024
CATALOG_TIMEOUT_SECONDS = 15
TAG_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]{0,31}")
SECRET_PATTERNS = {
    "OpenAI API key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\b(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,})\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "local home path": re.compile(r"/(?:home|Users)/[^/\s\"']+"),
}


def repository_files(pattern: str) -> list[Path]:
    return sorted(path for path in ROOT.rglob(pattern) if ".git" not in path.parts)


def sensitive_content_errors(path: Path, text: str) -> list[str]:
    relative = path.relative_to(ROOT)
    errors = []
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{relative}: contains a possible {label}")
    return errors


def fetch_node_types(url: str) -> set[str]:
    """Fetch the public catalog once; never upload example contents."""
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("catalog URL must be HTTP(S) without embedded credentials")
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=CATALOG_TIMEOUT_SECONDS) as response:
        body = response.read(CATALOG_MAX_BYTES + 1)
    if len(body) > CATALOG_MAX_BYTES:
        raise ValueError("node catalog exceeds the 5 MiB response limit")
    catalog = json.loads(body)
    if not isinstance(catalog, list):
        raise ValueError("node catalog must be an array of manifests")
    node_types = set()
    for index, manifest in enumerate(catalog):
        node_id = manifest.get("node_id") if isinstance(manifest, dict) else None
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError(f"node catalog entry {index} needs a non-empty node_id")
        node_types.add(node_id)
    return node_types


def load_node_manifests(directory: Path) -> dict[tuple[str, str], dict]:
    """Load wrapped node manifests from an unreleased local Subfork checkout."""
    if not directory.is_dir():
        raise ValueError(f"node catalog directory does not exist: {directory}")
    manifests: dict[tuple[str, str], dict] = {}
    for path in sorted(directory.rglob("node.subfork.node.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        manifest = document.get("node") if isinstance(document, dict) else None
        if not isinstance(manifest, dict):
            raise ValueError(f"{path}: expected a node manifest wrapper")
        node_id, version = manifest.get("node_id"), manifest.get("version")
        if not isinstance(node_id, str) or not isinstance(version, str):
            raise ValueError(f"{path}: manifest needs string node_id and version")
        key = (node_id, version)
        if key in manifests:
            raise ValueError(f"duplicate local node manifest {node_id}@{version}")
        manifests[key] = manifest
    if not manifests:
        raise ValueError(f"no node manifests found below {directory}")
    return manifests


def _manifest_ports(manifest: dict, direction: str) -> dict[str, str]:
    value = manifest.get(direction, {})
    if not isinstance(value, dict):
        return {}
    return {
        str(name): str(spec.get("type", "json") if isinstance(spec, dict) else spec or "json")
        for name, spec in value.items()
    }


def node_contract_errors(relative: Path, definition: dict, manifests: dict[tuple[str, str], dict]) -> list[str]:
    errors: list[str] = []
    nodes = definition.get("nodes", [])
    ports: dict[str, tuple[dict[str, str], dict[str, str]]] = {}
    instances = {
        node.get("node_instance_id"): node
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("node_instance_id"), str)
    }
    for node_id, node in instances.items():
        type_id, version = node.get("node_id"), node.get("node_version")
        manifest = manifests.get((type_id, version))
        if manifest is None:
            errors.append(f"{relative}: node {node_id!r} uses unknown local node version {type_id!r}@{version!r}")
            continue
        inputs = _manifest_ports(manifest, "inputs")
        parameters = manifest.get("parameters", {})
        if isinstance(parameters, dict):
            inputs.update({
                str(name): str(spec.get("type", "str"))
                for name, spec in parameters.items()
                if isinstance(spec, dict) and spec.get("exposable")
            })
            unknown = set(node.get("params", {})) - set(parameters) if isinstance(node.get("params", {}), dict) else set()
            if unknown:
                errors.append(f"{relative}: node {node_id!r} has unknown parameter {sorted(unknown)[0]!r}")
        outputs = _manifest_ports(manifest, "outputs")
        custom_inputs = node.get("custom_inputs", {})
        custom_outputs = node.get("custom_outputs", {})
        if custom_inputs and not manifest.get("dynamic_inputs"):
            errors.append(f"{relative}: node {node_id!r} does not accept custom inputs")
        if custom_outputs and not manifest.get("dynamic_outputs"):
            errors.append(f"{relative}: node {node_id!r} does not accept custom outputs")
        if isinstance(custom_inputs, dict):
            collisions = set(inputs) & set(custom_inputs)
            if collisions:
                errors.append(f"{relative}: node {node_id!r} custom input conflicts with {sorted(collisions)[0]!r}")
            inputs.update({str(name): str(kind) for name, kind in custom_inputs.items()})
        if isinstance(custom_outputs, dict):
            collisions = set(outputs) & set(custom_outputs)
            if collisions:
                errors.append(f"{relative}: node {node_id!r} custom output conflicts with {sorted(collisions)[0]!r}")
            outputs.update({str(name): str(kind) for name, kind in custom_outputs.items()})
        ports[node_id] = (inputs, outputs)
        for name in node.get("exposed_inputs", []) or []:
            if name not in inputs:
                errors.append(f"{relative}: node {node_id!r} exposes unknown input {name!r}")
        for name in node.get("exposed_outputs", []) or []:
            if name not in outputs:
                errors.append(f"{relative}: node {node_id!r} exposes unknown output {name!r}")

    for index, edge in enumerate(definition.get("edges", [])):
        if not isinstance(edge, dict):
            continue
        source_id, target_id = edge.get("source_node_id"), edge.get("target_node_id")
        if source_id not in ports or target_id not in ports:
            continue
        source_name, target_name = edge.get("source_output"), edge.get("target_input")
        source_type = ports[source_id][1].get(source_name)
        target_type = ports[target_id][0].get(target_name)
        if source_type is None:
            errors.append(f"{relative}: edge {index} uses unknown source port {source_id}.{source_name}")
        elif target_type is None:
            errors.append(f"{relative}: edge {index} uses unknown target port {target_id}.{target_name}")
        elif source_type != target_type and target_type != "any":
            errors.append(
                f"{relative}: edge {index} cannot connect {source_id}.{source_name} ({source_type}) "
                f"to {target_id}.{target_name} ({target_type})"
            )
        target = instances.get(target_id, {})
        if isinstance(target.get("literal_inputs"), dict) and target_name in target["literal_inputs"]:
            errors.append(f"{relative}: edge {index} and a literal both bind {target_id}.{target_name}")

    for name, binding in definition.get("graph_outputs", {}).items():
        if not isinstance(binding, dict):
            continue
        node_id, output_name = binding.get("node_instance_id"), binding.get("output_name")
        if node_id in ports and output_name not in ports[node_id][1]:
            errors.append(f"{relative}: graph output {name!r} uses unknown port {node_id}.{output_name}")
    return errors


def validate(path: Path, node_types: set[str] | None = None, node_manifests: dict[tuple[str, str], dict] | None = None) -> list[str]:
    relative = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    errors = sensitive_content_errors(path, text)
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        return errors + [f"{relative}: invalid JSON: {exc}"]
    if not isinstance(document, dict):
        return errors + [f"{relative}: document root must be an object"]
    if document.get("format") != "subfork.graph/1":
        errors.append(f"{relative}: format must be subfork.graph/1")
    tags = document.get("tags")
    if not isinstance(tags, list):
        errors.append(f"{relative}: tags must be a list")
    else:
        if len(tags) > 12:
            errors.append(f"{relative}: tags may contain at most 12 values")
        if len(tags) != len(set(tags)):
            errors.append(f"{relative}: tags must be unique")
        for tag in tags:
            if not isinstance(tag, str) or not TAG_PATTERN.fullmatch(tag):
                errors.append(f"{relative}: tags must be lowercase 1-32 character slugs")
    definition = document.get("definition")
    if not isinstance(definition, dict):
        return errors + [f"{relative}: definition must be an object"]
    if not isinstance(definition.get("name"), str) or not definition["name"].strip():
        errors.append(f"{relative}: definition.name must be a non-empty string")
    nodes = definition.get("nodes")
    edges = definition.get("edges")
    if not isinstance(nodes, list) or not nodes:
        errors.append(f"{relative}: definition.nodes must be a non-empty list")
        nodes = []
    if not isinstance(edges, list):
        errors.append(f"{relative}: definition.edges must be a list")
        edges = []
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue  # The instance-ID check below reports non-object nodes.
        node_type = node.get("node_id")
        if not isinstance(node_type, str) or not node_type.strip():
            errors.append(f"{relative}: node {index} needs a non-empty string node_id")
        elif node_types is not None and node_type not in node_types:
            errors.append(f"{relative}: node {node.get('node_instance_id', index)!r} uses node type {node_type!r} absent from the target catalog")
    node_ids = [node.get("node_instance_id") for node in nodes if isinstance(node, dict)]
    if len(node_ids) != len(nodes) or any(not isinstance(value, str) or not value for value in node_ids):
        errors.append(f"{relative}: every node needs a string node_instance_id")
    if len(node_ids) != len(set(node_ids)):
        errors.append(f"{relative}: node_instance_id values must be unique")
    known = set(node_ids)
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"{relative}: edge {index} must be an object")
            continue
        if edge.get("source_node_id") not in known:
            errors.append(f"{relative}: edge {index} has an unknown source node")
        if edge.get("target_node_id") not in known:
            errors.append(f"{relative}: edge {index} has an unknown target node")
        if not isinstance(edge.get("source_output"), str) or not edge["source_output"]:
            errors.append(f"{relative}: edge {index} needs a string source_output")
        if not isinstance(edge.get("target_input"), str) or not edge["target_input"]:
            errors.append(f"{relative}: edge {index} needs a string target_input")
    graph_outputs = definition.get("graph_outputs")
    if graph_outputs is not None and not isinstance(graph_outputs, dict):
        errors.append(f"{relative}: definition.graph_outputs must be an object")
    elif isinstance(graph_outputs, dict):
        for name, binding in graph_outputs.items():
            if not isinstance(name, str) or not name:
                errors.append(f"{relative}: graph output names must be non-empty strings")
            if not isinstance(binding, dict):
                errors.append(f"{relative}: graph output {name!r} must be an object")
                continue
            if binding.get("node_instance_id") not in known:
                errors.append(f"{relative}: graph output {name!r} has an unknown node")
            if not isinstance(binding.get("output_name"), str) or not binding["output_name"]:
                errors.append(f"{relative}: graph output {name!r} needs a string output_name")
    if node_manifests is not None:
        errors.extend(node_contract_errors(relative, definition, node_manifests))
    notes = path.with_name(path.name[: -len(".subfork.json")] + ".notes.md")
    if not notes.is_file():
        errors.append(f"{relative}: missing companion {notes.name}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    catalog = parser.add_mutually_exclusive_group()
    catalog.add_argument("--node-catalog-url", metavar="URL", help="also check node types against a target instance's /api/v1/nodes catalog (15s socket timeout, 5 MiB limit)")
    catalog.add_argument("--node-catalog-dir", metavar="DIR", type=Path, help="validate versions, parameters, exposed ports, edges, and outputs against local unreleased node manifests")
    args = parser.parse_args(argv)
    errors = []
    node_types = None
    node_manifests = None
    if args.node_catalog_url:
        try:
            node_types = fetch_node_types(args.node_catalog_url)
        except (OSError, URLError, ValueError) as exc:
            errors.append(f"could not validate against node catalog: {exc}")
    if args.node_catalog_dir:
        try:
            node_manifests = load_node_manifests(args.node_catalog_dir.resolve())
            node_types = {node_id for node_id, _version in node_manifests}
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"could not load local node catalog: {exc}")
    files = sorted(GRAPH_ROOT.rglob("*.subfork.json")) if GRAPH_ROOT.is_dir() else []
    if not GRAPH_ROOT.is_dir():
        errors.append("missing graphs directory")
    elif not files:
        errors.append("no example graph documents found")
    for path in files:
        errors.extend(validate(path, node_types, node_manifests))
    for path in repository_files("*.md"):
        errors.extend(sensitive_content_errors(path, path.read_text(encoding="utf-8")))
    if errors:
        print("Example validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(files)} Subfork example graphs.")
    if node_manifests is not None:
        print(f"Checked full contracts against the local catalog ({len(node_manifests)} node versions).")
    elif node_types is not None:
        print(f"Checked node types against the target catalog ({len(node_types)} available types).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
