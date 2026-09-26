# Contact CSV Deduplicator

<a href="../contact-csv-deduplicator.subfork.json" download="contact-csv-deduplicator.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Uploads a UTF-8 CSV contact list, projects a small field set, removes exact
duplicate email values, sorts by last name, and returns at most 250 rows.

Use these exact, case-sensitive headers:

```text
first_name,last_name,email,phone,company
```

The graph reads the uploaded asset through its temporary Subfork URL with a
20-second timeout and 1 MB response cap. It does not call a third-party provider,
send messages, modify contacts, or export to an address book.

Deduplication is exact and keeps the first occurrence. It does not trim fields,
lowercase email addresses, validate addresses or phone numbers, or merge partial
records. For example, `ADA@example.com` and `ada@example.com` remain separate.

Expected outputs are `contacts`, uploaded `filename`, fetch `status`, and a JSON
`response`. Bind `contacts` to a Table panel. Contact lists contain personal data:
use a synthetic or authorized file, review execution retention, and do not
publish a graph that contains a real uploaded contact asset.

The structure and node contracts were validated against the production catalog
on September 26, 2026. Upload and execution still need a local-development smoke
test before this example is described as manually run.
