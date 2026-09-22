# World Bank Population History

<a href="../world-bank-population-history.subfork.json" download="world-bank-population-history.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches the ten most recent non-empty annual observations for the World Bank
indicator `SP.POP.TOTL` for the United States. The World Bank JSON response is a
two-element array: request metadata followed by observation rows. The graph
selects element `1`, projects five columns, sorts by year, and applies a second
local limit.

This graph is keyless, read-only, and performs one request to
`api.worldbank.org`. The request asks for ten rows and uses a 20-second timeout
and 300 KB response cap. Run the graph again to retrieve a newer snapshot; it
does not poll in the background.

Expected outputs are `rows`, provider `status`, and a JSON `response`. Bind
`rows` to a Table panel. Published indicator values may be estimated or revised,
and the latest available year may lag the current year. World Bank API terms and
data attribution requirements apply.

Source: [World Bank Indicators API query structure](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581).
The endpoint was live-tested with the documented ten-row bounds on September 21,
2026.
