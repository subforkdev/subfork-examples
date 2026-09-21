# AI Example Instructions

- Place graphs and companion notes together in `image/`, `video/`, `audio/`,
  or `3d/` according to their main output. Update the subcategory's `README.md`
  and the graph index when adding an example. Each subcategory README becomes
  its landing page in MkPages; navigation is configured in `mkpages.yml`.
- Never include provider keys, user IDs, uploaded private assets, or generated
  media in an export.
- Name required execution-profile secrets exactly in the companion notes.
- Document that provider calls may cost money and identify externally visible or
  long-running operations.
- Prefer generic HTTP, job, and artifact primitives over provider-specific core
  behavior when the graph remains understandable.
- Keep optional media inputs optional and validate provider-facing URLs.
