# Podcast Episode Browser

<a href="../podcast-episode-browser.subfork.json" download="podcast-episode-browser.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches a public podcast RSS or Atom feed, parses the first 20 entries, and
renders their titles, publication strings, summaries, and episode-page links.
The default is NASA's **Houston, We Have a Podcast** feed.

This graph is keyless and read-only. The request uses a 20-second timeout and a
2 MB response cap. Run it again to refresh the snapshot. Feed order is preserved;
the graph does not sort or interpret publication dates.

The current RSS/Atom Parse node normalizes `title`, `url`, `id`, `summary`, and
`published`. It does not expose podcast enclosure URLs, durations, artwork, or
audio MIME types, so this is an episode browser rather than an audio player.
Summaries are displayed as plain text and truncated to 600 characters in the
HTML view. Only HTTP and HTTPS episode links become clickable.

Expected outputs are `episodes`, `html`, provider `status`, and an HTML
`response`. Public feeds can move, reject automated requests, change schema, or
contain copyrighted descriptions. Review the publisher's terms before
republishing feed content.

Source: [NASA RSS feeds](https://www.nasa.gov/rss-feeds/). The default feed URL
returned a bounded RSS payload on September 26, 2026. The graph structure and
node contracts were validated against the production catalog; an imported
Subfork execution still needs a local-development smoke test.
