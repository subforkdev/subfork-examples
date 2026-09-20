# Regional Watch

Import `regional-watch.subfork.json` **with recommended panels** and Run.
No new runtime node, API rebuild, or API key is needed. Existing imports are not
automatically updated.

The 48-node graph fetches USGS M2.5+ events from the past seven days, normalizes
and validates coordinates/numeric ranges, sorts newest first, limits to 1,000,
and adds region tags. Outputs are ordinary `events` and raw source `metadata`.
There is no dashboard envelope, embedded HTML, or service-specific panel logic.

## Graph-Authored Regions

Each region is a branch of existing **Filter Rows** nodes for latitude and
longitude bounds, followed by **Map Fields** preserving the event fields and
adding a literal `regions` array. Edit filter comparison values to change bounds,
and the projection's `regions` list to change its label. Then rerun the graph.
The Pacific branch concatenates longitude >= 120 and longitude <= -70, rather
than treating the date-line-crossing area as an ordinary range.

**Concat Lists** defines priority: North America, South America, Europe &
Mediterranean, Asia, Pacific / date line, then Other. **Unique** by `id` keeps
the first matching row. A fallback projection includes every source event with
`["Other"]`, so unmatched events survive. Final sorting restores newest-first
order. Each event appears once with exactly one region tag, even in overlaps.

These inclusive rectangular bounds are approximate, not authoritative continent
or jurisdiction borders. Longitude comparisons use the supplied numeric value;
there is no special normalization of equivalent -180/+180 coordinates.

The Regions facet derives menu entries and counts from actual event tags in the
completed snapshot. Regions without assigned events will not appear. Multiple
selected regions are ORed; other facets combine with AND. Table and Details
also expose the Regions field. No frontend region special case is involved.

This is deliberately a graph-only prototype, not a compact reusable region
algorithm. Adding a region requires another branch and a concatenation step;
changing priority requires rewiring concatenation inputs. Supporting arbitrary
region definitions or multiple tags per event elegantly remains future work.

## Native Panels

- Filters: search plus Regions, Location, Magnitude, Depth and Event time facets.
  Configure bindings controls the fields; Settings contains Reset filters.
- Metrics: matching count, maximum magnitude, latest event and activity histogram.
- Map Preview: filtered records with selected marker highlighting.
- Data Table: sortable columns; click or Enter/Space to select an event.
- Details: follows map/table selection and links to the source event.

All five bind to `sample.items` with identity field `id`, sharing selection and
filter state. Column labels, mappings and facet configuration are saved in the
recommended layout. Metrics uses `metadata.value.generated` for its histogram.
Numeric timestamps use an explicit date facet override, with UTC range inputs.

## Snapshot Semantics And Limits

Run the graph to fetch new data. Filters operate locally without graph execution.
Only a completed execution replaces the displayed snapshot; the prior snapshot
remains while running or after failure. New completed snapshots reset local
filters and selection. Source/freshness banners are intentionally absent.
This is manual-refresh exploration, not real-time monitoring or risk assessment.

The fetch is capped at 1 MB. Input ranges are longitude -180..180, latitude
-90..90, depth -10..800 km and magnitude 2.5..10. The graph limits to 1,000 rows;
generic panels support at most 10,000 records and 2 MB per collection. Empty
results are valid. Duplicate/missing IDs disable linked selection, not display.
OpenStreetMap tiles can still load when panning or zooming.

Tests cover graph execution with a fixture feed, region boundaries/overlaps,
date-line behavior, generic facet filtering and recommended layout round trips.

[USGS source and format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

See [dashboard architecture](../../docs/planning/subfork-dashboard-snapshots.md).
