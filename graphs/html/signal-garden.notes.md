# Signal Garden

A 2D botanical interpretation of real data. Each record becomes an interactive
SVG flower, with mapped stem height, bloom size, and petal color. This prototype
uses the same normalized USGS earthquake dataset as Planet Pulse, demonstrating
two different renderers for the same data without Three.js or a model API.

## Try It

1. Import `graphs/html/signal-garden.subfork.json` and run it.
2. Bind HTML Preview to `view.html` if the recommended layout is not applied.
   Maximize the panel for the full garden; narrow screens can scroll the canvas.
3. Change the height, size, color, or palette controls. Select a flower or its
   specimen-index button to inspect the source record. Flowers support keyboard
   focus, Enter, and Space as well as pointer selection.
4. Pause the swaying using Pause motion. Browser reduced-motion preferences
   disable animation automatically, including when changed while the page is open.

No additional application changes or rebuild are needed if dev already supports
the `html_safe` JSON Stringify option used by Planet Pulse. No API key is needed.
Each execution makes one bounded USGS request (30 seconds, 5 MB maximum). The
rendered page makes no network requests and loads no external scripts or fonts.

## Visual Mappings

- Stem height defaults to age in hours relative to source generation time:
  older records are taller.
- Bloom size defaults to reported magnitude: larger values produce larger blooms.
- Petal color defaults to depth in km, divided into three equal-width bins over
  the displayed range. This is not Planet Pulse's fixed 70/300 km depth scale.
- Numeric fields can be remapped across all three channels. String category
  fields can also control color; categories cycle through the three palette colors.
- Layout and petal count are decorative, deterministically seeded per record.
  Position is not geography; animation is not live activity or measured growth.

Scales use the displayed records, not a fixed cross-execution baseline. Equal
numeric values use the midpoint. Missing height/size values use a neutral midpoint;
missing color values are gray. Field notes identify unreported values.

The garden displays at most the newest 60 object records and reports truncation
and invalid rows. Records without timestamps sort after dated records. Empty
datasets show an explicit empty state. The snapshot timestamp is UTC; a warning
appears when it is more than two hours old. Rerun to refresh the underlying data.

## Reuse And Editing

The renderer's `dataset_json` input accepts HTML-safe serialized JSON containing:

- `rows`: a list of objects with numeric fields and optional category strings.
- `generated_at_ms`: source snapshot timestamp in Unix milliseconds.
- Optional `source` and `units` metadata.
- Row labels are taken from `place`, `name`, `title`, or `id`.
- Optional row `time` values are Unix milliseconds and produce `age_hours`.

The renderer contains no GeoJSON-specific parsing. Replace the upstream dataset
branch to use another source while retaining HTML-safe JSON serialization before
the template. Untrusted strings are rendered as text, not interpreted as markup.
The default branch emits the same `planet-pulse/1` dataset as Planet Pulse.

Outputs are `html`, HTML `response`, `dataset`, JSON `data_response`, `rows`, and
raw `geojson`. UI mappings affect only the HTML view, not those data outputs.
This is an ordinary-node prototype; no composite publication or graph IDs are
required. The dataset and renderer are candidates for separate composites later.

The graph JSON is the single source of truth. Edit the formatted HTML/CSS/JS in
the HTML node editor, save, and export to update the repository. There is no
separate renderer source directory or committed builder.

## Verification

Development smoke checks executed the graph with a synthetic HTTP response and
checked rendering, selection, mappings, palettes, motion preferences, missing/empty
data, and the record limit using a DOM stub. Shared HTML-safety tests also pass.
These are not browser visual tests or proof of live USGS availability. This
example adds no dedicated runtime test suite; verify visual edits by importing
and running the graph in the dashboard.
