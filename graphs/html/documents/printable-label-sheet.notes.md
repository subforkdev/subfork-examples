# Printable Label Sheet

<a href="../printable-label-sheet.subfork.json" download="printable-label-sheet.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Uploads a UTF-8 address CSV and renders at most 60 records as print-friendly,
three-column mailing labels. Use these exact headers:

```text
name,address1,address2,city,region,postal_code,country
```

The graph reads the uploaded asset through its temporary Subfork URL with a
20-second timeout and 1 MB response cap. It does not validate, standardize, or
geocode addresses. Blank fields are omitted, rows retain their input order, and
the first 60 rows are rendered.

Expected outputs are `rows`, `html`, uploaded `filename`, fetch `status`, and an
HTML `response`. The recommended HTML panel uses letter-size print CSS with 30
labels per page, but printers apply their own margins and scaling. Print a test
page on plain paper before using label stock. This example does not generate a
PDF or send data to a mailing provider.

Address files contain personal data. Use synthetic or authorized records,
review artifact and execution retention, and do not publish a graph containing
a real uploaded file.

The structure and node contracts were validated against the production catalog
on September 26, 2026. Upload, rendering, and physical print alignment still
need a local-development smoke test.
