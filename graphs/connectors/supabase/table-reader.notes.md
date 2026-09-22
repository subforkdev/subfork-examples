# Supabase Table Reader

<a href="../table-reader.subfork.json" download="table-reader.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Reads a bounded set of rows from one Supabase table or view through the Data REST
API.

Before running:

1. In the HTTP Request node, replace `PROJECT_REF` and `RELATION` in the URL with
   your project reference and a URL-safe table or view name. Make this edit before
   publishing the graph as a composite so its destination remains fixed.
2. Add the project's `sb_publishable_...` key as the graph-scoped secret
   `SUPABASE_PUBLISHABLE_KEY`.
3. Confirm that Row Level Security policies reveal only the intended rows and
   columns. Never substitute a secret or service-role key in this example.

The graph requests `select=*` with `limit=25`, then applies a second local limit
of 25. It uses a 20-second timeout and a 500 KB response cap and does not follow
pagination. The request URL is not a composite input, so clients cannot replace
the reviewed destination with a host that would receive the API key.

Expected outputs are `rows`, provider `status`, and a JSON `response`. Bind
`rows` to a Table panel. The graph performs no writes, but its execution output
contains every column returned by the configured relation and RLS policy.
Supabase service limits and account terms apply. No live Supabase request was
made while authoring this example.

Provider references: [Data REST API](https://supabase.com/docs/guides/api) and
[API keys](https://supabase.com/docs/guides/getting-started/api-keys).
