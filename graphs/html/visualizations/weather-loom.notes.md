# Weather Loom

A year of daily station weather rendered as an interactive SVG textile. Months
run downward and days of the month run left to right. The default is NOAA's
San Francisco International Airport station, year 2024, including February 29.

## Try It

1. Import `graphs/html/visualizations/weather-loom.subfork.json` and run it.
2. Bind HTML Preview to `view.html` if the recommended layout is not applied.
3. Maximize the panel. Select a day or use Inspect date for its measurements.
4. Change the color variable, palette, rain shaping, wind texture, or units.
5. For another station/year, edit the Station and year JSON Value node and rerun.
   Keep the station ID as an 11-digit string so leading zeros are preserved.

No API key or additional application rebuild is required if the runtime already
supports HTML-safe JSON Stringify. The single graph JSON contains the formatted
HTML/CSS/JS template; edit it in the node editor and export to update the repository.
There is no separate source directory, committed builder, or runtime test suite
for this example. No new platform features or hosting behavior were implemented.

## Data And Limits

Source: [NOAA NCEI Global Summary of the Day](https://www.ncei.noaa.gov/access/search/datasets/global-summary-of-the-day/).
The default direct CSV is
[station 72494023234, 2024](https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/72494023234.csv).
Use the dataset search to find other station IDs; changing a place label alone
does not change the data source. A nonexistent station/year file fails visibly.

The graph makes one HTTP request, with a 40-second timeout and 2 MB response
limit, parses CSV, projects relevant fields, and assembles an HTML-safe dataset.
The browser makes no data, font, script, or basemap requests. Controls only affect
the current snapshot. Dates are NOAA GMT/UTC daily summaries, not browser-local
dates. Precipitation periods may overlap the previous day.

Open-Meteo was considered but not used: its
[free API terms](https://open-meteo.com/en/terms) exclude commercial products and
promotional use. This prototype avoids depending on that API or a subscription.
No NOAA endorsement is implied. Station observations are not city-wide averages.

## Reading The Weave

- Thread color defaults to daily mean temperature. Precipitation and mean wind
  are alternatives, with five equal-width color bins over available yearly values.
- Reported precipitation bends the horizontal threads using a bounded logarithmic
  mapping. Rain shaping adjusts the artistic exaggeration, not the underlying data.
- Wind adds up to five cross-stitches per day (one per four source knots).
- Absent days and missing color values show gray hatching, never an invented zero.
- Missing rainfall causes no bending and missing wind no cross-stitches, but
  the daily details distinguish missing measurements from reported zero values.
- Metric display converts Fahrenheit to Celsius, inches to mm, and knots to km/h.
  Conversion does not change the underlying source measurements or visual encoding.

The renderer follows NOAA's [format documentation](https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt):
temperature sentinel 9999.9, precipitation 99.99, and mean wind 999.9 become missing.
Empty strings are also missing. Negative rain/wind values are rejected. Precipitation
flags H (incomplete/possible trace), I (no precipitation data), or unknown flags
are excluded from quantitative color and shaping. A-F can describe sub-daily
reporting intervals; G is a reported 24-hour amount. The selected-day details show
the flag and caveat. No certified annual precipitation total is calculated.

The calendar always shows 365 or 366 slots for the configured year. Missing days
remain in their correct positions; nonexistent dates such as April 31 have no
slot. Foreign-station, invalid-date, out-of-year, and duplicate records are skipped
and counted. The renderer accepts years 1929-2100 and reports invalid configuration.
This is descriptive artwork, not a forecast, climate trend, or safety product.

## Outputs And Verification

Outputs: `html`, HTML `response`, projected `rows`, `dataset`, JSON `data_response`.
The `weather-loom/1` dataset preserves original numeric strings, sentinels, and
precipitation flags alongside config, source URL, source units, and timezone.
Unit conversion and missing-value interpretation occur in the renderer, not in
the projected data output; downstream consumers must apply those rules themselves.

On September 14, the fetched NOAA 2024 CSV contained 366 records. A graph smoke
execution with that response verified the CSV/transform/template pipeline. DOM-stub
checks passed for leap-day selection, all presentation controls, empty records,
missing sentinels, incomplete precipitation, and literal unsafe station text.
These are not browser screenshot tests; import/run the graph to verify appearance.
