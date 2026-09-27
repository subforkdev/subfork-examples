# GitHub Release Dashboard

<a href="github-release-dashboard.subfork.json" download="github-release-dashboard.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches and normalizes one bounded page of releases for a public GitHub repository,
then presents the records through linked Filters, Metrics, Table, and Details
panels. The default source is `cli/cli`.

## Configure And Run

1. Import the graph with its recommended layout.
2. Change **GitHub releases URL** to
   `https://api.github.com/repos/OWNER/REPOSITORY/releases` when needed.
3. Run the graph, filter by author, prerelease state, or publication date, and
   select a row to inspect its release notes and GitHub link.

The graph requests page 1 with `per_page=30`, applies a 20-second timeout, caps the
response at 1 MB, limits to 30 rows, and sorts by `published_at` descending. It
normalizes `id`, `tag`, `title`, `author`, `published_at`, `created_at`, `url`,
`prerelease`, `draft`, and `body`. It does not paginate, fetch tag-only releases,
or calculate download totals from nested assets.

This example is keyless and read-only. GitHub applies unauthenticated rate limits
and may change its API behavior. No credentials, paid services, or external writes
are used. The public endpoint was checked during authoring; a fresh Subfork import,
execution, and panel interaction test remain manual.
