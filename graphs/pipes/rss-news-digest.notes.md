# RSS News Digest

## What This Template Proves

This is the simplest Yahoo Pipes-style digest path: collect rows, filter by topic, sort by rank, limit, and expose a response.

## Current Behavior

The graph is runnable today because feed items are mocked as a `JSON Value`.

Expected output is a list of `subfork` topic items sorted by descending score.

## Faked Pieces

- RSS/Atom fetching is represented by mocked JSON.
- Feed parsing is not implemented.
- This seed's digest rendering is JSON-only; the platform's HTML Template node
  and HTML/Markdown preview panels are available for a future revision.

## Missing Nodes And Panels

- RSS/Atom Fetch or Feed Fetch node
- Feed Parse / Normalize Items node
- Template Render node
- Table panel as a first-class importable template dependency
- HTML/Markdown preview panel binding as template metadata

## Architecture Implications

Templates need to declare requirements before import/fork. The graph can be runnable with mocked data, but the real template needs network capability and feed parsing support.
