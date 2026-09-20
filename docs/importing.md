# Importing Examples

Subfork graph imports replace the graph currently loaded in the editor. Create a
new graph first if the current graph contains work you want to keep.

1. Open the example's `*.notes.md` file and review its requirements.
2. Download the adjacent `*.subfork.json` file.
3. In Subfork, create or open the destination graph.
4. Open Graph Settings, select **Import**, and choose the JSON file.
5. Inspect the graph before running it. In particular, review HTTP destinations,
   exposed responses, and provider-backed nodes.
6. Configure any documented execution-profile variables or secrets.
7. Save the imported graph, run it, and inspect its panels and outputs.

## Trust And Secrets

Graph JSON is executable configuration. Only import files you trust, and review
network requests and scripts just as you would review source code.

Exports must not contain secret values. Examples refer to secrets by stable names
such as `OPENAI_API_KEY`; add the actual value in the destination graph's
execution profile. Never paste a key into a Value, Template, URL, or script node.

## Compatibility

Examples currently use the `subfork.graph/1` export format. If an import fails,
update Subfork first and check the example's recent history. A successful import
does not guarantee that external providers or public datasets are currently
available.
