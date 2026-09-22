# Connector Example Instructions

- Keep provider credentials in graph-scoped execution-profile secrets and name
  each required secret in the companion notes.
- Pin credential-bearing requests to the provider's origin. Do not expose their
  complete URL as a composite input; use execution-profile variables for bounded
  resource identifiers when the URL must vary.
- Bound every read with provider query limits, timeouts, and response-size caps.
- Make external writes unmistakable in the graph name, description, and notes.
  Document retry and duplication risks; never run live writes during validation.
- Prefer generic HTTP and transformation nodes while the provider operation stays
  understandable. Record OAuth, pagination, signing, or multipart gaps explicitly.
- Give composite-ready connectors a small typed interface and preserve raw provider
  responses only when they are useful for inspection.
