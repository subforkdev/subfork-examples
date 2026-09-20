# News Constellation

Three tech-related RSS feeds become a selectable SVG star atlas. Articles are
grouped by source, not AI-inferred topic. This prototype remains in the SVG
gallery track and requires neither an AI service nor an API key.

## Try It

1. Import `graphs/html/news-constellation.subfork.json` and run it.
2. Bind HTML Preview to `view.html` if the recommended layout is not applied.
3. Maximize the panel, search headlines, filter a source, or toggle the lines.
4. Select a star or headline-index button to inspect its source and feed date.
   Stars support focus, Enter, and Space. The index offers an accessible alternative.
5. Focus the Article URL field to select its text, then copy it into another tab.

The current HTML Preview sandbox blocks new tabs; this example deliberately does
not loosen that sandbox or change the existing Open in new tab action. It provides
a selectable URL instead of a broken outbound-link button. Stable hosting and
public sharing remain separate planned features.

No extra application rebuild is needed when the runtime already supports HTML-safe
JSON Stringify. The graph JSON is self-contained with a formatted, editable HTML
template; there is no separate source folder or committed generator.

## Sources

- [Hacker News RSS](https://news.ycombinator.com/rss): community-submitted links
  from its feed, not every submission, votes, comments, or a full article archive.
- [Ars Technica all-news RSS](https://feeds.arstechnica.com/arstechnica/index):
  technology reporting; listed on its [feed directory](https://arstechnica.com/rss-feeds/).
- [GitHub Blog RSS](https://github.blog/feed/): developer-focused posts with a
  vendor perspective, not an independent news publication.

Each branch performs one public HTTP read (30-second timeout, 2 MB body limit),
parses RSS, and projects only title, URL, ID, and publication date into the shared
dataset. No linked pages are fetched. The rendered output includes no article
bodies, feed summary markup, tracking images, external scripts, or fonts.
Raw fetched/parsing outputs can still be present in the private execution record.

Edit a branch's URL Input node to change the feed; also update its source label
in the dataset template. The v1 renderer expects exactly three feed groups.
This graph uses RSS endpoints verified with the existing parser; arbitrary Atom
feeds may need review of their link/date conventions before substitution.

Public RSS is a discovery mechanism, not a blanket content-republication license.
Retain attribution and source URLs and review publisher terms before public or
commercial gallery deployment. The example itself does not publish anything.

## Visual Contract

The renderer keeps at most the first 24 valid unique article URLs per feed, up to
72 total. It reports additional items, invalid entries, and within-feed duplicates.
HTTP(S) URLs must parse and contain no username/password; fragments are removed
for within-feed deduplication. Articles shared by different feeds remain visible
in both source groups. This is not semantic duplicate detection.

Default list order preserves source grouping and feed order, which may be ranked
rather than chronological. Newest dated first reorders only the bounded display
set, with undated items last; it does not query the publishers for more results.
Search is case-insensitive headline matching across that same set.

Positions are deterministic for a given feed ordering and remain stable while
filtering or changing list order. Connecting lines link nearby visible members
of the same feed; they do not encode topic relationships. All article stars have
the same size, with source-specific colors. Faint background dust is decoration,
not additional articles. Selecting a star highlights its corresponding list item.

Publication dates come only from parsed feed fields and are shown in UTC. Missing
or invalid dates are explicitly unavailable; retrieval time is not substituted.
HTTP response dates, when available, are separately labeled. Rerun to refresh;
the page never fetches fresh data on its own. Empty results are explicit.

If any feed fetch/parse fails, the graph does not produce a new combined snapshot.
There is no silent fallback to cached or invented feed content and no claim of
partial-feed recovery in v1. Inspect the execution failure and retry or change
the affected source. Publisher availability and rate limits can vary.

## Outputs And Verification

Outputs: `html`, HTML `response`, `dataset`, and JSON `data_response`.
The `news-constellation/1` envelope contains three labeled feed groups with URLs,
response headers, and projected items. The full projected item set remains in
the dataset; the 24-item cap and URL filtering apply in the renderer.

On September 14, live fetches returned 30 HN items, 20 Ars items, and 10 GitHub
Blog items. A graph smoke execution using those fetched responses passed all
three parse/project branches and HTML response generation. DOM-stub checks
covered search, source filtering, ordering, connections, selection, empty data,
missing dates, unsafe URLs, deduplication, and literal unsafe headline text.
These are not browser visual tests or guarantees of future source availability.
No prototype-specific tests were added to the application runtime suite.
