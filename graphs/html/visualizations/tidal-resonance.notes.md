# Tidal Resonance

NOAA tide predictions from San Francisco (9414290), Seattle (9447130), and
The Battery, New York (8518750) become three flowing SVG ribbons. A shared time
scrubber reveals how their predicted heights differ throughout one returned UTC
day. This is an educational visualization, not an observation, weather forecast,
storm-surge forecast, or navigation/safety tool.

## Try It

1. Import `graphs/html/visualizations/tidal-resonance.subfork.json` and run it.
2. Bind HTML Preview to `view.html` if the recommended layout is not applied.
3. Scrub through the day, isolate a station, switch meters/feet, or change palette.
4. Inspect the exact selected six-minute sample in the station cards. The slider
   supports keyboard interaction; narrow screens scroll the chart horizontally
   while the cards stack vertically.

No API key, Three.js, or AI service is required. No application rebuild is needed
if HTML-safe JSON Stringify is already available. The single JSON contains a
formatted, editable HTML template. Custom inputs are explicitly exposed and the
unused HTML `context` input is hidden. No source folder or generator is committed.

## Sources And Data Contract

Uses the [NOAA CO-OPS Data API](https://api.tidesandcurrents.noaa.gov/api/prod/).
Each of three branches makes one request with `product=predictions`, `date=today`,
`interval=6`, `time_zone=gmt`, `datum=MLLW`, `units=metric`, and JSON format.
Requests have a 30-second timeout and 500 KB body limit. There is no polling,
pagination, or browser-side request. Rerun the graph to refresh.

`today` is resolved by the provider; the page labels the actual returned UTC date,
not the browser's date or timezone. To request a fixed date, replace `date=today`
in each URL with matching `begin_date=YYYYMMDD&end_date=YYYYMMDD`. Keep units,
datum, interval, and timezone unchanged unless also updating the renderer's
contract. To change a station, update its URL and its name/ID in the dataset node.

The `tidal-resonance/1` envelope contains three labeled station payloads, HTTP
statuses, source URLs, and headers, with declared meters/MLLW/UTC semantics.
JSON parsing happens in the graph. Validation, time alignment, unit conversion,
and ribbon construction happen in the renderer. The dataset retains raw NOAA
prediction records; view validation does not silently rewrite its source output.

## Visual Meaning And Limits

Each ribbon connects valid six-minute samples in time order. Height uses a shared
linear scale computed across all valid station samples, including zero. The scale
stays fixed when a station is isolated. Filled areas extend to each station's
local MLLW zero; **these are different local reference datums**, not one global
sea-level surface. Negative predictions are retained and mean below local MLLW,
not negative water depth. Color only distinguishes stations.

The time scrubber selects exact samples, not an interpolated measurement.
Straight connecting segments are visual interpolation. Sampled min/max values
are not exact high/low tide times. The browser never invents extra predictions
or synthesizes fallback tides. There is no animation or hidden autoplay.

The renderer expects three station groups and at most 240 records per group.
It validates UTC date strings, six-minute alignment, numeric meter heights within
an intentionally generous +/-100 m bound, and duplicate timestamps. It reports
invalid/off-day, duplicate, and over-cap records. The first usable station sets
the displayed UTC day; other-day samples are excluded and reported, preventing
silent alignment across midnight. Missing intervals split the paths instead of
connecting across gaps. Missing selected-time samples say Unavailable.

HTTP/API errors with parseable JSON can produce partial station output with a
visible warning; if all stations are unusable the page shows an error instead of
a fabricated chart. An execution can complete with an error page because status
codes are data. Transport or JSON-parse failures fail the graph and do not produce
a new combined artifact. There is no cached-source recovery policy in this seed.

Source text is inserted with `textContent`, and dataset embedding uses
`html_safe=true`. The page has no external scripts, fonts, or images. Validated
NOAA station URLs are shown as copy fields because new tabs are blocked by the
current preview sandbox. Hosting and form-triggered execution remain separate
planning work; this prototype does not change sandbox permissions.

## Outputs And Validation

Outputs: `html`, HTML `response`, `dataset`, and JSON `data_response`.
Fourteen runtime nodes replayed three freshly fetched NOAA responses, each with
240 predictions, through dataset and response generation. Renderer checks covered
unit conversion, time endpoints, palettes, station isolation, gaps, duplicate and
invalid samples, literal hostile text, and partial/all-source failures.
Desktop and narrow-screen output were inspected with headless Chrome; a dashboard
import/run remains the final manual check. No application code or permanent
prototype-specific runtime tests were added.
