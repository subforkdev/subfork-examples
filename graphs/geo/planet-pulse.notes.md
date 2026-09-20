# Planet Pulse

An importable, keyless USGS earthquake observatory. This first version uses real
public earthquake data, not simulated weather or invented telemetry. It does not
require Three.js, published composite dependencies, or a paid service.

## Try It

1. Rebuild dev first: this graph uses the new opt-in `html_safe` parameter on
   JSON Stringify. The parameter escapes HTML delimiters without changing the
   decoded JSON value; existing JSON Stringify behavior is unchanged by default.
2. Import `graphs/geo/planet-pulse.subfork.json` through Import graph.
3. Run the graph. Open/bind HTML Preview to `view.html` if the recommended panel
   layout is not applied. Maximize that panel for the full observatory layout.
4. Filter to 24/12/6/1 hours, change the minimum magnitude, rotate the longitude
   slider, or select a recent event to bring it onto the near hemisphere.
5. Optionally bind Map Preview to `parse.value` for a street-map geographic view,
   Table to `rows.items`, and JSON to `dataset.value`.

The source is the USGS M2.5+ past-day GeoJSON feed. Each execution makes one
bounded public HTTP request (30-second timeout, 5 MB response limit). There are
no browser-side data requests in the HTML view and no model/API keys to supply.
Map Preview, if opened, separately loads its normal basemap tiles.

## What It Shows

- An orthographic SVG globe with latitude/longitude grid and embedded Natural
  Earth coastline outlines (not terrain or political boundaries).
- Marker radius derived from magnitude; depth colors split at 70 and 300 km.
- Filtered event count, maximum magnitude, and newest-first event list.
- Source snapshot timestamp and event timestamps in UTC, with an old-snapshot
  warning when opened more than two hours after source generation.
- Selected-event coordinates, depth, and a validated USGS HTTPS link.

This is a snapshot, not a live subscription. Rerun to refresh. The time filters
are relative to source generation time, so reopening an artifact preserves its
meaning. Counts cover both hemispheres; the globe draws only the near hemisphere.
The list shows the newest 100 matching records and explicitly reports truncation.
The globe uses all matching valid records. Missing magnitude/time/depth or invalid
coordinates are omitted from the visualization and counted in its notice.

The HTML Preview sandbox currently blocks new-window navigation, so source links
may need to be copied/opened manually from the preview. Standalone HTML supports
the links. This example does not loosen the application's iframe sandbox.

## Reuse And Publication

Outputs include `html`, HTML `response`, raw `geojson`, projected `rows`,
`dataset`, and JSON `data_response`. The `planet-pulse/1` dataset envelope contains
source URL, generation time, window, units, timezone, and rows with:

`id`, `place`, `magnitude`, `time`, `lon`, `lat`, `depth_km`, `url`.

Projected rows preserve source null values for downstream consumers; the globe
validates and omits unusable records separately. Depth is km and time is Unix ms.
The HTML filter controls affect only that view, not graph dataset outputs.

Before extracting/publishing composites, stabilize this contract. A later data
composite can expose the dataset to other renderers, including Three.js. Today
the HTML branch consumes the same source snapshot through HTML-safe JSON because
it also needs the GeoJSON validation and provider metadata. No publishing occurs
automatically, and local/production graph IDs are not embedded in this file.

## Editing And Tests

The template has normal newlines and indentation in Subfork's code editor.
JSON represents those newlines as `\n` inside its string, so editing the raw
JSON file is not the intended authoring workflow. Edit the HTML node in Subfork
and save/export the graph. `planet-pulse.subfork.json` is the single source of
truth; there is no separate template source folder or build step. In-app edits
must be exported back to that file to update the repository.

The shared HTML-safe JSON behavior has an independent fixture at
`backend/runtime/tests/fixtures/html_safe.json`, with tests for opt-in behavior,
round-trip preservation, and safe embedding in an HTML template:

```sh
PYTHONPATH=backend/runtime python -m pytest backend/runtime/tests/test_html_safe.py -q
```

Planet Pulse has no dedicated automated graph/renderer suite. Verify edits by
importing and running the graph, checking filters, rotation, event selection,
and empty results. The runtime tests do not check live USGS availability or
visual appearance. No PNG/PDF export, scheduled refresh, or alerting is promised.

## Coastline Data

The embedded `coastlines` node contains a coordinate-only conversion of Natural Earth's
[1:110m coastline dataset](https://www.naturalearthdata.com/downloads/110m-physical-vectors/110m-coastline/),
downloaded from the project's
[GeoJSON distribution](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_coastline.geojson)
on 2026-09-13. Coordinates are rounded to three decimal places; all 134 lines
and 5,128 points are retained. Natural Earth data is
[public domain](https://www.naturalearthdata.com/about/terms-of-use/).

The graph stores it in a separate JSON Value node, then serializes it with
HTML-safe JSON Stringify. It does not add a runtime network dependency or put
thousands of coordinates in the editable HTML template. The globe interpolates
segments at one-degree intervals and breaks paths on the far hemisphere.

For an already-running dev build with HTML-safe JSON support, this refinement
only needs a fresh graph import and execution, not an application rebuild.
