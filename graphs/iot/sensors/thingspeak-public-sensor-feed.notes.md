# ThingSpeak Public Sensor Feed

<a href="../thingspeak-public-sensor-feed.subfork.json" download="thingspeak-public-sensor-feed.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Reads ten entries from ThingSpeak channel `9`, the public home-environment sensor
channel used in MathWorks' REST API documentation. It extracts the feed array and
projects timestamps, entry IDs, light readings, and outside-temperature readings.

This graph is keyless and read-only. The provider and local limits are both ten
rows, with a 20-second timeout and 300 KB response cap. ThingSpeak identifies
`field1` as Light and `field2` as Outside Temperature, but the channel response
does not declare reliable units, so the example labels both as raw values.

Expected outputs are `entries`, provider `status`, and a JSON `response`. Bind
`entries` to a Table panel. Public channels are owner-controlled and can become
stale, change fields, disappear, or contain unverified measurements. During the
September 21, 2026 live check, the ten returned observations were dated June 28,
2026; use this as an API-shape example rather than a current environmental feed.

Source: [ThingSpeak Read Data API](https://www.mathworks.com/help/thingspeak/readdata.html).
ThingSpeak licensing, caching, and service terms apply.
