# Environment Agency River Gauge

<a href="../environment-agency-river-gauge.subfork.json" download="environment-agency-river-gauge.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Reads the latest stage and flow telemetry from Environment Agency monitoring
station `2200TH` in England. The full response view provides the parameter,
qualifier, unit, reporting period, timestamp, and value for each measure.

This graph is keyless and read-only. It requests at most ten readings, applies a
second local limit of ten, and uses a 20-second timeout and 300 KB response cap.
The public API generally receives new measurements at 15-minute intervals, but
individual station transfers can be less frequent and responses may be cached.
Run the graph again to fetch a newer snapshot.

Expected outputs are `readings`, provider `status`, and a JSON `response`. Bind
`readings` to a Table panel. `mASD` is metres relative to the station's local
datum; it is not elevation above sea level. This beta feed has no service-level
guarantee and must not replace official flood warnings or safety channels.

Source: [Environment Agency real-time flood-monitoring API](https://environment.data.gov.uk/flood-monitoring/doc/reference).
This uses Environment Agency flood and river level data from the real-time data
API (Beta), available under the Open Government Licence. The endpoint was
live-tested on September 21, 2026.
