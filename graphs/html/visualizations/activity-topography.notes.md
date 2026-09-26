# Activity Topography

A public GitHub repository becomes a landscape of weekly SVG ridges. Daily
sampled commit counts set the heights; select a summit to inspect its commits.
The default repository is `psf/requests`. No API key, AI service, or Three.js is
required.

## Try It

1. Import `graphs/html/visualizations/activity-topography.subfork.json` and run it.
2. Bind HTML Preview to `view.html` if the recommended layout is not applied.
3. Maximize the preview. Try 12, 24, or 52 weeks, filter a contributor, change the
   palette, or adjust relief.
4. Select a peak using the mouse or Enter/Space, or use the active-day selector.
   Select a commit to inspect its subject, timestamp, SHA, and copyable URL.
5. To change repositories, edit the **Repository / owner and name** static-value
   node, for example `{"owner":"pallets","repo":"flask"}`, and rerun.

The file is self-contained with a formatted HTML template editable in Subfork's
HTML editor. There is no separate source folder or committed generator. No extra
application rebuild is needed if HTML-safe JSON Stringify is already available.
Custom inputs are explicitly exposed; the unused HTML `context` input is hidden.

## Source And Bounds

Uses GitHub's [List commits API](https://docs.github.com/en/rest/commits/commits#list-commits):
one GET for the default branch's first page, `per_page=100&page=1`, with a
30-second timeout and a 2 MB response limit. No pagination, repository checkout,
per-commit detail fetches, or browser-side requests. Public resources can be read
without authentication, but shared-IP rate limits apply. Renamed repositories
may require updating the configuration because the runtime does not follow
redirects. Private repositories are outside this keyless example's scope.

The graph projects SHA, committer timestamp, linked author login, commit message,
and HTML URL. It does not project author email, avatar, or signature fields into
the public dataset. Raw fetch/parse outputs still contain the provider's full
response and can remain in the private execution record. Commit messages are
public source text, not necessarily free of personal information; review before
publishing outputs. No output is published automatically.

The dataset retains HTTP status and response headers. A GitHub error response
with a JSON body produces an explicit error page, not an empty success landscape;
the graph execution can still complete because HTTP status is data. Network or
JSON parsing failures fail execution. There is no invented fallback dataset.

## Visual Contract

The renderer validates timestamps and SHAs, deduplicates by SHA, caps input at
100 records, and groups committer timestamps into UTC calendar days and
Monday-start weeks. Grouping is currently performed in the HTML renderer; the
JSON output is the projected commit snapshot, not the daily aggregation.

The displayed window ends in the latest valid commit's week, **not necessarily
the current week**. Its anchor stays fixed when filtering contributors. Every
ridge represents a week, oldest at the back and newest at the front, with days
running Monday to Sunday. Peak height is linear in daily count, normalized to
the maximum count in the current view and multiplied by the relief control.
Changing filters changes that scale; the numeric peak/day indicator reports the
current maximum. Color and perspective are aesthetic, not additional metrics.
Lines between the seven daily points are decorative interpolation.

Blank days mean no matching records in this bounded sample, not demonstrated
inactivity. Pagination, date ordering, rebases, merges, and the API page boundary
can limit coverage. The page reports omitted records, invalid or duplicate
entries, current filters, response time when available, and whether GitHub's
Link header identifies another page. It never claims a complete date interval.
Merge commits and bot contributions are included; counts are not effort,
quality, productivity, or lines changed.

Contributor filtering uses linked GitHub author logins; records without one are
grouped as **Unlinked author**, which may represent multiple people. The day
selector and commit list provide a keyboard-accessible alternative to small SVG
points. No animation or external fonts/scripts/images are required. Source text
uses `textContent`; the dataset is serialized with `html_safe=true` before being
embedded. Only validated HTTPS GitHub commit URLs appear in the copy field.

The current preview sandbox blocks new tabs. Select and copy the URL rather than
using a broken outbound link. Output hosting and the existing Open in new tab
action remain separate planned work.

## Outputs And Checks

Outputs: `html`, HTML `response`, `dataset` (`activity-topography/1`), and JSON
`data_response`. Source configuration and dataset assembly are separate graph
nodes so the renderer can later become a reusable component.

Validation included replaying 100 freshly fetched `psf/requests` commits through
all ten runtime nodes, empty and HTTP-error responses, and HTML-safe hostile
commit text. Renderer checks covered contributor/window/palette/relief controls,
selection, duplicate and invalid records, empty results, and unsafe URL rejection.
Desktop and narrow-screen output were checked in headless Chrome. These checks
do not guarantee future GitHub availability or replace a dashboard import test.
No application code or prototype-specific runtime test suite was added.
