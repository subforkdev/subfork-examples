# Seismic Depth Field

Import `seismic-depth-field.subfork.json` with its recommended panels and Run.
No API key or application rebuild is needed. The graph uses existing built-in
nodes only; there is no new renderer, embedded JavaScript, or HTML template.

## Data And Scene

One HTTP Request fetches the public [USGS GeoJSON summary feed](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
for M2.5+ earthquakes in the past seven days. Map / Project Fields extracts the
event ID, location, magnitude, timestamp, URL, longitude, latitude, and depth.
Numeric range filters exclude missing/out-of-range coordinates and magnitudes;
Sort Rows and Limit retain at most 1,000 newest valid events.

Three Compute Field nodes turn those records into positions:

- `x = longitude * 0.03`: east to the right.
- `y = depth_km * -0.008`: depth downward, deliberately exaggerated.
- `z = latitude * -0.03`: north toward the back in the authored coordinate frame.

Magnitude filters split the positions into three point geometries, each with its
own Material and Scene Object: mint M2.5 to <4, amber M4 to <5, coral M5+.
Group Scene Objects combines them with a graph-authored dotted reference grid.
The reference grid is static geometry data, not simulated or fetched geography.
Its zero-depth surface has 30-degree spacing; front depth guides mark 200, 400,
600, and 800 km. The entire group feeds Transform / Motion and Compose Scene.

Recommended panels: 3D Preview, Markdown Preview for the legend, and Data Table
for the source rows. A separate `metadata` output retains USGS feed generation
time and original event count; bind a JSON Inspector to it if useful.

## Controls And Limits

Drag to orbit, right-drag to pan, scroll to zoom. The panel settings menu contains
Play/Pause, Reset animation, Frame scene and Authored camera. Playback starts
paused and rotates the entire field; it does not replay earthquake times or
refresh the data. Run the graph again to fetch a new snapshot.

This is a flat longitude/latitude plot, not a globe, geological model or metric
projection. Degree distances vary with latitude, depth is exaggerated, and the
date line is a seam. Negative reported depths appear above the reference plane.
Point size encodes a magnitude band, not rupture extent or a linear energy scale.
The viewport does not yet provide point labels or hover inspection; use the
source table for event details.

Accepted ranges are longitude -180..180, latitude -90..90, depth -10..800 km and
magnitude 2.5..10. An empty valid feed renders only the reference grid. A failed
HTTP request fails the execution instead of silently displaying synthetic data.
The request is capped at 1 MB and 1,000 valid events are kept after sorting.

## Verification

Executed all 40 nodes against the live USGS feed and rendered the resulting
scene in headless Chrome. Also exercised the real graph executor with empty and
synthetic feeds: magnitude boundaries, missing/invalid values, negative depth,
coordinate mapping, and the 1,000-event cap. No prototype-specific runtime code
or renderer changes were required.

Useful next generic capabilities: per-point/instance attributes, hover metadata,
axis labels and line geometry. These should remain reusable scene primitives,
not earthquake-specific panel behavior.
