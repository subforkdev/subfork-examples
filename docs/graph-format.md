# Graph Document Format

Subfork examples use the portable `subfork.graph/1` JSON envelope. An agent can
author or adapt an example without access to the Subfork source tree, but it
must consult the production public node catalog for node-specific ports,
parameters, versions, and worker requirements. A local development catalog is
used only while testing unreleased changes.

## Minimal Shape

```json
{
  "format": "subfork.graph/1",
  "definition": {
    "version": "0.1.0",
    "name": "Example name",
    "description": "What the graph does and its important limits.",
    "nodes": [
      {
        "node_instance_id": "message",
        "node_id": "n_text_value",
        "node_version": "1.0.0",
        "title": "Message",
        "params": {
          "text": "Hello"
        }
      }
    ],
    "edges": [],
    "graph_outputs": {
      "text": {
        "node_instance_id": "message",
        "output_name": "text"
      }
    }
  }
}
```

Keep the envelope and exported field names exactly as shown. Start from the
closest existing example or a fresh Subfork export when possible. Do not invent
node IDs, parameter names, ports, or versions from memory.

## Definition Fields

- `version`, `name`, and `description` identify the graph document. Give the
  graph a concise name and describe network access, side effects, or important
  limits.
- `nodes` is a nonempty array of node instances. Every `node_instance_id` must
  be unique within the graph. `node_id` selects a node type from the target
  catalog, and `node_version` records the version used by the export.
- `params` contains node-specific configuration. Use only fields and values
  supported by the node manifest.
- `edges` connect an exact `source_output` to an exact `target_input`. The
  source and target IDs are node instance IDs, not node type IDs.
- `graph_outputs` gives stable names to selected node outputs. Each binding
  names an existing node instance and one of its outputs.
- `metadata` carries authoring and presentation hints. Existing examples use
  `metadata.template` for category, requirements, and a composite interface,
  and `metadata.canvas` for positions and recommended panels. Copy these shapes
  from a nearby example and omit optional hints that do not apply.

Some exported nodes include `custom_inputs`, `exposed_inputs`,
`exposed_outputs`, and matching visibility flags. Preserve these fields when
adapting an export. Add dynamic inputs only when the node manifest and a working
example show that the node supports them.

## Node Contracts

Fetch the production catalog before choosing or changing a node:

```sh
curl --fail --silent --show-error --max-time 15 --max-filesize 1048576 \
  https://subfork.com/api/v1/nodes/n_text_value
```

The single-node endpoint returns the matching manifest directly. Use the full
`/api/v1/nodes` collection when discovering available node IDs.

The manifest is authoritative for:

- `node_id` and current `version`;
- input and output port names and types;
- parameters, defaults, required values, and enumerated options;
- execution-profile schema and required worker capabilities;
- allowed placement.

The catalog at `subfork.com` is authoritative for released examples. A local
development instance may temporarily expose unreleased nodes during testing.
The examples repository does not vendor a catalog snapshot because it would
become stale and could incorrectly claim compatibility with production.

## Variables And Secrets

Configuration that differs by graph or execution belongs in graph-scoped
execution profiles. Examples use template references such as:

```text
{{ vars.AIRTABLE_BASE_ID }}
{{ secrets.AIRTABLE_ACCESS_TOKEN }}
```

Use these references only in parameters that support template expansion. List
every required variable and secret in the companion notes and in
`metadata.template.requires` when that metadata is present. Never put a secret
value, private URL, account identifier, cookie, or local path in graph JSON.

Credential-bearing HTTP requests should keep the provider origin fixed. Vary
bounded resource identifiers through variables instead of accepting an
arbitrary URL that could receive the credential.

## Agent Authoring Workflow

1. Read the root and category-specific `AGENTS.md` files.
2. Choose the closest existing graph and read both its JSON and companion notes.
3. Fetch every proposed node manifest from `subfork.com`, or from local
   development when testing an unreleased node.
4. Build nodes with unique instance IDs and exact manifest parameters.
5. Connect exact output and input port names, checking their types.
6. Expose only useful graph outputs and add presentation metadata when it helps.
7. Add companion notes covering setup, network calls, bounds, costs, side
   effects, outputs, limitations, and test status.
8. Run offline validation and target-catalog validation:

   ```sh
   python3 scripts/validate_examples.py
   python3 scripts/validate_examples.py \
     --node-catalog-url https://subfork.com/api/v1/nodes
   ```

9. Import the result into a fresh graph in local development, then inspect it
   and run the documented happy path before describing it as tested.

Repository validation checks the envelope, references, common credential
patterns, and production node-type availability. It does not prove that parameters,
ports, provider behavior, costs, or side effects are correct. The target catalog,
a fresh import, and an appropriate manual run remain required for that evidence.
