# Earthquake Map

## What This Template Proves

This probes whether Subfork should treat map output as a panel contract over typed values rather than a special graph response.

## Current Behavior

The graph imports and runs today, returning mocked GeoJSON through `JSON Response`.

## Faked Pieces

- Public USGS fetch is mocked in this fixture. Use `Live USGS Earthquake Map` for a remote public-data version.
- GeoJSON normalization is pre-baked into the static value.

## Missing Nodes And Panels

- GeoJSON Normalize node
- Optional Table panel binding metadata on import
- Better typed value metadata for `GeoJSON`

## Architecture Implications

Panels should declare supported value types. A single `GeoJSON` output should be bindable to map, table, and JSON views without adding map-specific behavior to data nodes.
