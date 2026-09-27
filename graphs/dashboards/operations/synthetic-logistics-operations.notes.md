# Synthetic Logistics Operations Dashboard

<a href="synthetic-logistics-operations.subfork.json" download="synthetic-logistics-operations.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

A deterministic command-center dashboard built from 30 bundled synthetic shipment
records. It demonstrates shared filtering and selection across native Metrics,
Map, Table, and Details panels without exposing real routes, customers, cargo, or
provider credentials.

## Run And Inspect

1. Import the graph with its recommended layout and run it.
2. Filter by status, priority, facility, carrier, delay, or estimated arrival.
3. Select a shipment in the map or table; the Details panel follows the same
   stable `id`.
4. Edit records in **Synthetic shipment fixture** to explore different scenarios.

The graph sorts by `delay_minutes` descending and limits output to 40 records. Its
included fixture contains 30. Fields are `id`, `shipment`, `status`, `priority`,
`origin`, `destination`, `facility`, `carrier`, `latitude`, `longitude`,
`planned_arrival_ms`, `estimated_arrival_ms`, `delay_minutes`, `exception`,
`progress_percent`, and `synthetic`.

The snapshot is fictional and fixed at 2026-09-26 16:00 UTC. Coordinates are
illustrative positions, arrival estimates are fixture values, and delay metrics
are not operational predictions. There are no network calls, credentials, paid
services, external writes, or persistent state. Route lines, playback, live
telemetry, and dispatch actions are outside this example.

Repository validation checks structure and panel bindings; a fresh dashboard
import and linked-selection smoke test remain manual.
