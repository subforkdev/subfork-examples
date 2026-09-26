# Plain HTTP Response

## What This Template Proves

This probes the generic response-envelope contract. A graph can store status,
content type, headers, and body directly in node params for a future HTTP endpoint.

## Current Behavior

The graph imports and runs without upstream nodes. Authoring execution produces a
response object with a `text/plain` body. Direct `/graphs/:id/response` delivery
is currently disabled (503); this is not a publicly callable endpoint.

## Architecture Implications

Specialized response nodes like JSON, HTML, ICS, RSS, CSV, SVG, image, and media responses should become presets or extension nodes that emit the same envelope rather than special cases in Subfork core.
