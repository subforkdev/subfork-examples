# Other Worlds / Exoplanet Portrait

A Dataset Portrait prototype using NASA's Exoplanet Archive rather than the
earthquake dataset. Each planet is a selectable radial mark with remappable
spoke length, mark size, color, and clockwise ordering. No Three.js or API key.

## Try It

1. Import `graphs/html/exoplanet-portrait.subfork.json` and run it.
2. Bind HTML Preview to `view.html` if the recommended layout is not applied.
3. Maximize the preview, remap the channels, change the palette, and select a
   mark or planet-index button to inspect the measurements. Marks support focus,
   Enter, and Space. The index remains usable when marks overlap.

No additional rebuild is needed if the current runtime already supports the
`html_safe` JSON Stringify parameter used by the other prototypes. The graph JSON
is the single source of truth: edit the formatted template in the node editor
and export the graph to update the repository. No source folder or builder is
required to use it. There are no browser-side network requests or external fonts.

## Source And Selection

Data comes from the NASA Exoplanet Archive's
[HTTP TAP service](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html),
using the `ps` Planetary Systems table. The query selects default parameter sets
with `default_flag=1`, excludes contested entries with `pl_controv_flag=0`, and
requires reported distance greater than zero and less than 20 parsecs.

The graph sorts the returned records by distance and limits them to 96 before
normalization. It does not rely on the archive's TOP ordering behavior. This is
a bounded nearby sample, not a representative population or complete census.
The HTTP request has a 45-second timeout and 2 MB response limit; exceeding it
fails rather than silently truncating the JSON. Run again to refresh.

The default PS parameter set is used instead of combining parameter estimates
from different references in the PSCompPars table. Missing fields remain missing.
See NASA's [table and field definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_TD_columns.html).

NASA Exoplanet Archive is operated by Caltech/IPAC for NASA. No NASA endorsement
of this visualization is implied. The graph preserves the query and source in
its dataset output. If present, the HTTP response Date is displayed as such; it
is not labeled as the measurement date or archive-wide last-update time.

## Reading The Portrait

- Spoke length defaults to orbital period in days; alternatives are radius or distance.
- Mark radius defaults to planetary radius in Earth radii; alternatives are period or distance.
- Length and mark radius use log(1 + value) scaling over the selected sample,
  not physical scale or an area-proportional encoding. Equal values use the midpoint.
- Color defaults to estimated equilibrium temperature in kelvin, with three
  equal-width bins. Alternatives are discovery year or discovery method.
- Missing and limit-only size values are hollow fixed-size marks. Missing and
  limit-only lengths use dashed short spokes. Missing color values are gray.
- The data retains NASA's radius, period and temperature limit flags. Only
  measurements with flag zero and positive finite values are used in those mappings.
- Discovery-method colors cycle through the palette and are listed explicitly.
- Order starts at the top and proceeds clockwise. Unknown sort values come last.

The portrait is not an orbital simulation or sky map. Color is not observed
planet color. Equilibrium temperature is not surface temperature or evidence of
habitability. Measurement uncertainties are not plotted; use the archive for
scientific analysis. Data labels are inserted as text, not HTML.

## Reusable Outputs

Outputs: `html`, HTML `response`, normalized `rows`, `dataset`, JSON `data_response`.
The `exoplanet-portrait/1` dataset includes source, selection query, units, response
headers, and rows with name, host, method, discovery year, radius, orbital period,
equilibrium temperature, distance, and measurement-limit flags. The renderer
consumes this normalized envelope rather than raw NASA column names.

UI mappings do not change graph data outputs or submit another execution. Hosting,
stable sharing URLs, and query-input mapping remain separate planned features.

## Verification

On September 14, the distance-bounded live query returned 291 records. An offline
graph execution using that fetched response sorted/limited them to 96, starting
with Proxima Cen b, and produced the dataset and HTML response. DOM-stub checks
covered all mappings/sorts/palettes, selection, empty/missing/limit-only data, and
unsafe label text. These are not browser visual tests or an ongoing availability
guarantee. No dedicated prototype tests were added to the runtime suite.
