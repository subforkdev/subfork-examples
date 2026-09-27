# Data Aquarium

<a href="data-aquarium.subfork.json" download="data-aquarium.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Upload an arbitrary UTF-8 CSV and turn up to 100 rows into a deterministic Canvas
aquarium. Each fish represents one row. Choose a label field, then find the ten
requested specimens by matching the requested value to the compact label rendered
under each fish. Labels follow the selected field and truncate after 18 characters.

## Try It

1. Import the graph and upload a CSV in **Upload aquarium CSV**.
2. Run the graph and open the recommended HTML Preview.
3. Select any detected column as the fish label and play the expedition.
4. Inspect the bounded parsed rows in the JSON panel.

CSV Parse reads the upload directly from Subfork artifact storage through an
execution- and attempt-scoped grant with a 1 MB limit. It accepts UTF-8 CSV with
an optional byte-order mark. The graph retains at most 100 rows and does not route
the private artifact through HTTP Request. Gameplay, animation, scoring, and field
selection run locally in the rendered page and make no network requests. Identical
rows and field selection produce the same initial fish placement and mission order.

The rendered HTML contains the uploaded rows so the browser can play the game.
Treat its preview/output as private when the CSV contains confidential or personal
data, and do not publish it unintentionally. Labels and record details are inserted
with DOM text APIs rather than interpreted as HTML.

There are no credentials, paid calls, sound, server-side scores, leaderboards, or
persistent state. Empty CSVs and unusable columns show an error. Repository checks
cover graph structure and script syntax; touch/keyboard accessibility and actual
play after a fresh import remain manual checks.
