# Published Sheet Mail Merge Preview

<a href="../mail-merge-preview.subfork.json" download="mail-merge-preview.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches a Google Sheet that its owner has published as CSV and renders up to 50
personalized message previews. It never connects to Gmail and does not send,
schedule, track, or save email drafts.

Replace the placeholder URL with the published CSV URL for the intended sheet
and worksheet. Use these headers:

```text
email,first_name,company,subject,message
```

`email`, `subject`, and `message` are displayed as plain text. When `subject` or
`message` is blank, the preview uses clearly marked sample copy derived from
`first_name` and `company`. Edit the HTML Template node if you want a different
shared fallback message.

The graph is keyless and read-only. Publishing a sheet may make its contents
broadly accessible. Do not publish recipient lists or confidential message copy
to the web. The request has a 20-second timeout and 1 MB response cap, and the
graph retains only the first 50 rows. Google publishing delays, availability,
terms, and quotas apply.

Expected outputs are `rows`, `html`, provider `status`, and an HTML `response`.
The recommended HTML panel is print-friendly, but printing or saving a PDF is a
browser action outside graph execution.

The structure and node contracts were validated against the production catalog
on September 26, 2026. No live Google request or email action was performed while
authoring this example.
