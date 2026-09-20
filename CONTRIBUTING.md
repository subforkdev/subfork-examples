# Contributing

Contributions should make an example easier to import, understand, or safely
adapt. Small, focused pull requests are preferred.

Unless explicitly stated otherwise, contributions intentionally submitted for
inclusion are provided under the repository's [Apache License 2.0](LICENSE), as
described in Section 5 of that license. Contributions must not include third-party
material that cannot be distributed under those terms.

## Workflow

1. Import and fork the closest existing example in Subfork, or create a new graph.
2. Export the graph as `<name>.subfork.json` into the appropriate `graphs/` category.
3. Add or update `<name>.notes.md` using the checklist in
   [Authoring examples](docs/authoring.md).
4. Remove credentials, account identifiers, private endpoints, and incidental
   execution data from the export.
5. Run `python3 scripts/validate_examples.py`.
6. Import the saved file into a fresh graph and run the documented happy path.

Include the Subfork version used for manual testing and note any provider calls,
costs, or features that could not be exercised. Screenshots are optional and
must not contain private account or execution data.

Repository validation checks document structure and common secret patterns. It
does not prove that a graph is safe, affordable, or compatible with every
Subfork release; contributors and reviewers remain responsible for those checks.
