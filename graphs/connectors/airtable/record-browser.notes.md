# Airtable Record Browser

<a href="../record-browser.subfork.json" download="record-browser.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Reads a bounded page of records from one Airtable table.

Before running:

1. Add `AIRTABLE_BASE_ID` and `AIRTABLE_TABLE_ID` as graph-scoped execution-profile
   variables. Use Airtable's `app...` and `tbl...` IDs.
2. Add `AIRTABLE_ACCESS_TOKEN` as a graph-scoped execution-profile secret. Use a
   personal access token restricted to the required base and read-only records scope.

The graph requests at most 25 records with a 20-second timeout and a 500 KB
response cap. Airtable may paginate list responses; this example intentionally
does not follow an `offset`, so it is a record browser rather than a full sync.
The credential-bearing request remains pinned to `api.airtable.com`; callers of a
published composite cannot replace it with a URL that would receive the token.

Expected outputs are `records`, provider `status`, and a JSON `response`. Bind
`records` to a Table panel. The graph performs no writes, but it reads data from
the configured base and may expose those records in execution output. Airtable
API limits and account terms apply. No live Airtable request was made while
authoring this example.
