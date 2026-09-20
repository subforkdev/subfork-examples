# URL Extract Pipe

## What This Template Proves

This validates text transformation with regex extraction and shows how a generic grep-like node can support Yahoo Pipes-style workflows.

## Current Behavior

The graph imports and runs today. It stringifies a JSON value, extracts URLs with `Text Match`, and returns the matches as JSON.

## Faked Pieces

The source text is static. A real template would often start from RSS, HTML, uploaded text, or fetched web content.

## Missing Nodes And Panels

- Text Input node
- HTML/Text Fetch node
- More structured regex capture outputs
- Table/List panel for match inspection

## Architecture Implications

Regex extraction should stay a reusable transform primitive. Richer source nodes and panels can make it useful without making the node provider-specific.
