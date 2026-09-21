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


def validate(path: Path, node_types: set[str] | None = None) -> list[str]:
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
    notes = path.with_name(path.name[: -len(".subfork.json")] + ".notes.md")
    if not notes.is_file():
        errors.append(f"{relative}: missing companion {notes.name}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node-catalog-url", metavar="URL", help="also check node types against a target instance's /api/v1/nodes catalog (15s socket timeout, 5 MiB limit)")
    args = parser.parse_args(argv)
    errors = []
    node_types = None
    if args.node_catalog_url:
        try:
            node_types = fetch_node_types(args.node_catalog_url)
        except (OSError, URLError, ValueError) as exc:
            errors.append(f"could not validate against node catalog: {exc}")
    files = sorted(GRAPH_ROOT.rglob("*.subfork.json")) if GRAPH_ROOT.is_dir() else []
    if not GRAPH_ROOT.is_dir():
        errors.append("missing graphs directory")
    elif not files:
        errors.append("no example graph documents found")
    for path in files:
        errors.extend(validate(path, node_types))
    for path in repository_files("*.md"):
        errors.extend(sensitive_content_errors(path, path.read_text(encoding="utf-8")))
    if errors:
        print("Example validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(files)} Subfork example graphs.")
    if node_types is not None:
        print(f"Checked node types against the target catalog ({len(node_types)} available types).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
