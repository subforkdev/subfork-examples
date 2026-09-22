# Current Weather Snapshot

<a href="../current-weather-snapshot.subfork.json" download="current-weather-snapshot.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches current Open-Meteo conditions for Seattle coordinates and turns the
provider's `current` object into a one-row table. Edit `latitude` and `longitude`
in the HTTP Request query to use another location. Keep a single coordinate for
this graph because multi-coordinate responses have a different shape.

This graph is keyless and read-only. It performs one request to
`api.open-meteo.com`, asks only for six current variables and one forecast day,
and uses a 20-second timeout and 200 KB response cap. Run it again to refresh the
snapshot; it does not poll in the background.

Expected outputs are `conditions`, provider `status`, and a JSON `response`.
Bind `conditions` to a Table panel. Times are UTC; temperature is Fahrenheit,
wind is miles per hour, and precipitation is inches. `weather_code` is a WMO
code and is intentionally left numeric. Forecast and current-condition values
are model-derived and should not be treated as emergency guidance. Review
Open-Meteo licensing, attribution, fair-use, and commercial-use terms for your
deployment.

Source: [Open-Meteo Forecast API](https://open-meteo.com/en/docs). The endpoint
was live-tested with the documented bounds on September 21, 2026.
