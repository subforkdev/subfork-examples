# Public Data Example Instructions

- Use public, documented endpoints that require no account or credential.
- Keep provider origins fixed and bound remote results with query limits, short
  timeouts, response-size caps, and a local row limit where the response is a list.
- State the source, update cadence or freshness caveat, units, and interpretation
  limits in the companion notes.
- Treat each execution as a snapshot. Do not use asynchronous job polling nodes to
  simulate scheduled data refreshes.
- Project provider payloads into small table-ready rows while preserving source
  identifiers and links when they help users verify a record.
