# AI Example Instructions

- Never include provider keys, user IDs, uploaded private assets, or generated
  media in an export.
- Name required execution-profile secrets exactly in the companion notes.
- Document that provider calls may cost money and identify externally visible or
  long-running operations.
- Prefer generic HTTP, job, and artifact primitives over provider-specific core
  behavior when the graph remains understandable.
- Keep optional media inputs optional and validate provider-facing URLs.
