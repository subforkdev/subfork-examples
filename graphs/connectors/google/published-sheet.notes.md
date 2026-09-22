# Published Google Sheet

<a href="../published-sheet.subfork.json" download="published-sheet.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches a Google Sheet that its owner has explicitly published to the web, parses
the CSV response, and returns at most 100 rows. Replace the placeholder URL with
the CSV URL for your published sheet and worksheet (`gid`).

This example is keyless and read-only. Publishing a sheet can make its contents
available broadly on the web, depending on the owner's account settings. Do not
use it for private or sensitive data. Edits to the source sheet can appear in the
published version after Google's publishing delay.

The HTTP request uses a 20-second timeout and a 1 MB response cap; the collection
step retains only the first 100 parsed rows. It does not use the private Google
Sheets API or OAuth. Expected outputs are `rows`, provider `status`, and a JSON
`response`. No live Google request was made while authoring this example.
