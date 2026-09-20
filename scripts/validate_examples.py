#!/usr/bin/env python3
"""Validate portable Subfork example documents without application dependencies."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
GRAPH_ROOT = ROOT / "graphs"
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


def validate(path: Path) -> list[str]:
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


def main() -> int:
    errors = []
    files = sorted(GRAPH_ROOT.rglob("*.subfork.json")) if GRAPH_ROOT.is_dir() else []
    if not GRAPH_ROOT.is_dir():
        errors.append("missing graphs directory")
    elif not files:
        errors.append("no example graph documents found")
    for path in files:
        errors.extend(validate(path))
    for path in repository_files("*.md"):
        errors.extend(sensitive_content_errors(path, path.read_text(encoding="utf-8")))
    if errors:
        print("Example validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(files)} Subfork example graphs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
