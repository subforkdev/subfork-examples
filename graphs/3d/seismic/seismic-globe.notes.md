# Seismic Globe

## Linked Selection And Columns

The three instance mappings preserve each event's `id` as `record_id`. The
recommended 3D panel keeps `compose.scene` as its data binding and links its
interaction source to `sample.items` (identity field `id`). Import with recommended
panels and rerun to produce identified geometry. Existing imported graphs and
historical execution artifacts are not automatically rewritten: add
`"record_id": "id"` to shallow/intermediate/deep instance mappings and configure
the 3D interaction source, or re-import the updated example.

Table selection highlights matching geometry; clicking a visible spike selects
its row. Selection does not rotate the globe. Focus is a separate, opt-in generic
object-framing action, not an occlusion-aware globe orbit. Events on the far side
may require manually orbiting the globe. A future generic radial-focus mode
should be explicit rather than embedding seismic/globe-specific camera code.

Data Table **Settings > Columns** toggles visible columns, including the ID column
without disabling record selection. Save the graph/layout to persist the choices;
they also travel with exported/recommended panel layouts. Hiding a column does not
remove the underlying data or hide it from Details/other panels.

Rebuild the application/runtime for Spherical Coordinates and extended instance
transforms, then import `seismic-globe.subfork.json` with recommended panels and
Run. No API key is required. Seismic Depth Field remains a separate example.

## Pipeline

The graph fetches the USGS M2.5+ seven-day summary, projects source fields,
filters invalid/out-of-range values, sorts newest first and caps the scene at
1,000 events. It retains the same source table and metadata output as the depth
field. One HTTP request is made per run; there are no per-frame requests.

Compute Field produces `height = 0.25 * magnitude - 0.5` and then
`radius = 3.001 + height/2`. Spherical Coordinates projects each event and emits
an outward-facing rotation. Map / Project Fields assembles position, rotation,
and scale records for instances of a shared unit box. The box's local Y scale
is height; its width and thickness are 0.025. Accounting for half-height places
the spike's base on the radius-3 globe, rather than burying half the spike.

Depth bands select materials: mint below 70 km, amber 70 to <300 km, rose 300 km
and deeper. Explicit `instanced: true` makes empty bands render no geometry.
The radius-3 sphere, sampled coastline dots, graticule and spikes are grouped
together and optionally rotated by Transform / Motion. No renderer code knows
about USGS, earthquakes, globes or this graph.

## Geography And Interpretation

The initial camera looks toward the eastern Pacific. Drag to orbit, right-drag
to pan, scroll to zoom. The panel settings menu controls playback and camera.
Playback starts paused and rotates the globe; it does not replay event times.

Spikes represent magnitude, not literal earthquake altitude, rupture extent,
or hypocenter depth. Their linear visual scale is not an energy scale. Depth is
encoded only by color, not by physically embedding earthquakes in the globe.
The 32-segment sphere is deliberately bounded; this is a visualization, not a
geodetic model. Graticule spacing is 30 degrees. +Y is north, +X is zero longitude,
and -Z is 90 degrees east. The Data Table and legend provide context; per-spike
hover/picking is not implemented yet.

The graph embeds 2,603 sampled longitude/latitude records from the Natural Earth
1:110m coastline, reusing the source downloaded for Planet Pulse. These are
static reference data inside the graph, not application assets. Every second
vertex of each coastline was retained; fine islands and coastline detail are
not reliable at this sampling. Both the coastline and graticule are projected
by the same Spherical Coordinates node used for events.

- [USGS GeoJSON summary format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
- [Natural Earth coastline](https://www.naturalearthdata.com/downloads/110m-physical-vectors/110m-coastline/)
- [Natural Earth public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/)

## Verification And Limits

All 52 nodes executed against the live USGS feed. The resulting scene rendered
in Chrome. Offline graph checks covered empty bands, depth boundaries, magnitude
height, the 1,000-event cap and the one-MB scene limit. Generic runtime/frontend
tests cover axes and poles, radial spike bases/tips, instance normalization,
invalid inputs, empty instancing and compatibility with legacy position arrays.

HTTP errors fail the execution; there is no silent synthetic-data fallback.
Coordinate filters retain longitude -180..180, latitude -90..90, depth -10..800 km
and magnitude 2.5..10. Reference geometry remains visible when no valid events
are present. Future additions should be generic scene features: picking metadata,
labels, line geometry and per-instance color, not special-case seismic code.
