# NASA Open Natural Events

<a href="../nasa-open-natural-events.subfork.json" download="nasa-open-natural-events.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches up to ten open natural events added or updated within the last 30 days
from NASA's Earth Observatory Natural Event Tracker (EONET). It selects the
`events` list and projects the first category, source, and geometry observation
from each event into a compact table row.

This graph is keyless and read-only. It performs one request to
`eonet.gsfc.nasa.gov` with provider and local limits of ten rows, a 20-second
timeout, and a 500 KB response cap. Run it again for a newer snapshot; there is
no background polling.

Expected outputs are `events`, provider `status`, and a JSON `response`. Bind
`events` to a Table panel. Events can contain multiple categories, sources, and
geometry observations; this introductory example keeps only the first of each.
Magnitude units vary by event type and may be absent. EONET is a discovery feed,
not an emergency warning service; follow the included source URL for context.

Source: [NASA EONET API v3](https://eonet.gsfc.nasa.gov/docs/v3). The endpoint was
live-tested with `status=open`, `days=30`, and `limit=10` on September 21, 2026.
