# Agent Instructions

This repository contains public, portable Subfork examples. Keep changes scoped
to examples, their documentation, and repository validation.

## Required Practices

- Read [Graph document format](docs/graph-format.md) before authoring or
  structurally changing a graph. It defines the local envelope and workflow;
  the production catalog remains authoritative for released node contracts.
- Before authoring or changing nodes in a graph, consult the production public
  JSON catalog: https://subfork.com/api/v1/nodes. Fetch one node at
  `https://subfork.com/api/v1/nodes/{node_id}`. Check ports, parameter schemas,
  defaults, versions, and worker requirements rather than guessing.
  Use a local development catalog only when testing an unreleased Subfork
  change. See [Node documentation](docs/authoring.md#node-documentation).
- Before duplicating a higher-level integration, inspect the production public
  composite catalog at
  `https://subfork.com/api/v1/graphs/published`. Prefer a compatible published
  graph-backed node over copying its lower-level provider implementation.
  Choose `latest` or `pinned` deliberately and document the update policy.
- Never commit credentials, access tokens, cookies, private URLs, personal data,
  generated media, or local absolute paths.
- Keep secrets in graph-scoped execution profiles and reference them by name.
- Pair every runnable `<name>.subfork.json` with `<name>.notes.md`.
- Document network calls, provider requirements, costs, limits, and destructive
  or externally visible side effects.
- Prefer deterministic, keyless examples. Keep remote requests bounded by
  explicit timeouts, response-size limits, and row limits.
- Preserve the exported `subfork.graph/1` envelope. Do not hand-edit generated
  IDs unless the change is intentional and validated.
- Run `python3 scripts/validate_examples.py` before completing a change.
- When checking production compatibility, also run
  `python3 scripts/validate_examples.py --node-catalog-url https://subfork.com/api/v1/nodes`,
  substituting a local development URL only for unreleased changes. Report
  catalog failures or missing node types; do not treat an unavailable API as a
  pass.
- After changing site content or navigation, run
  `mkpages build . --output .mkpages`; never edit generated output directly.

Subdirectory `AGENTS.md` files add category-specific guidance and take precedence
for files in that directory.
