# Authoring Examples

An example should teach one clear composition pattern and remain understandable
after import. Prefer a small graph over a comprehensive workflow.

## Graph Checklist

- Use a concise graph name and description.
- Give every node a purpose-oriented title.
- Expose only useful graph outputs.
- Include a recommended panel layout when visualization is central to the example.
- Keep network calls bounded with timeouts and response-size limits.
- Limit remote rows before expensive transformations or rendering.
- Use graph-scoped variables for non-secret deployment configuration.
- Use graph-scoped secrets for credentials; never include secret values in JSON.
- Avoid account-specific IDs, unpublished URLs, and local filesystem paths.
- Import the final export into a fresh graph and run it.

## Notes Checklist

The companion notes should explain:

- purpose and data flow;
- whether the graph is keyless, local-only, or provider-backed;
- required variables, secret names, and worker capabilities;
- external endpoints, likely costs, side effects, and relevant terms;
- expected graph outputs and recommended panels;
- bounded-compute choices and known limitations;
- the Subfork version and scenario used for the latest manual test.

Design proposals may be notes-only, but should say explicitly that no importable
graph exists yet.
