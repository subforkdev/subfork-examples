# Live USGS Earthquake Map

This graph fetches public GeoJSON from the USGS earthquake feed and returns it directly for Map Preview, Table, and JSON panels.

The graph shape is:

`URL Input -> HTTP Request -> JSON Path -> JSON Response`

Recommended panel bindings:

- Map Preview: bind to `Fetch earthquakes: json`.
- Data Table: bind to `Feature rows: value`.
- JSON Inspector: bind to `GeoJSON Response: response` or `Fetch earthquakes: json`.

The default feed is:

`https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson`

You can edit the `USGS GeoJSON URL` node to try other USGS feeds such as all-day, significant-week, or monthly feeds.

Known v0 caveat: the Map Preview understands GeoJSON Point features and simple rows with lat/lon fields. Lines, polygons, clustering, heatmaps, and richer basemap controls are future panel upgrades.
