# Geo Situational Brief

This is a deliberately meaty graph template for exercising branching, filters, cross-referencing, and multiple panels.

The default graph fetches live USGS earthquake GeoJSON, reads profile variables for a reference location, filters significant events, finds the nearest earthquake to the reference location, cross-references a small static city list, produces chart buckets, and renders a Markdown brief.

Default profile variables:

- `USER_LAT`: `37.7749`
- `USER_LON`: `-122.4194`
- `MIN_MAGNITUDE`: `4.5`
- `MAX_EVENTS`: `12`

High-level shape:

```text
USGS GeoJSON URL -> HTTP Request -> Feature extraction
Feature extraction -> Significant GeoJSON -> Map / JSON Response
Feature extraction -> Top event rows -> Table / Markdown summary
Feature extraction + profile location + reference cities -> Nearest quake -> Nearest map layer
Feature extraction -> Magnitude buckets -> Chart
Feature extraction -> Region buckets -> Markdown summary
All summary branches -> Markdown brief -> Text Response
```

Recommended panels:

- Map Preview bound to `Significant GeoJSON: value`
- Map Preview bound to `Nearest map layer: value`
- Data Table bound to `Top event rows: value`
- Chart Preview bound to `Magnitude buckets: value`
- Markdown Preview bound to `Markdown brief: value`
- JSON Inspector bound to `Brief summary JSON: value`

Why this graph exists:

- It exercises remote HTTP data.
- It fans one dataset into multiple branches.
- It uses profile variables as stand-ins for future browser geolocation.
- It cross-references a static city dataset.
- It highlights where useful transforms should become first-class primitives later.

Future upgrades:

- Add a Browser Location input primitive that prompts for geolocation and passes `USER_LAT`/`USER_LON` into execution.
- Add a Geo Distance / Nearest Feature primitive.
- Add a GeoJSON Filter primitive.
- Add map panel configuration for auto-focus behavior, layers, clustering, and marker styling.
- Add default panel layout import so the recommended panels appear automatically.
