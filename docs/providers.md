# Provider Requirements

Most examples are keyless. Some fetch public datasets, and the `graphs/ai/` examples can
call paid provider APIs. Always inspect the companion notes before running one.

## OpenAI

The runnable OpenAI examples require a graph-scoped secret named
`OPENAI_API_KEY`. Configure it in Graph Settings under the execution profile.
The key is resolved by the worker and must never appear in graph JSON.

Image, speech, asset-pack, and video operations can incur charges. Video jobs are
long-running and their provider API may change or be retired; consult the
example's notes and current provider documentation before use.

## Public Data Sources

Several examples make bounded, unauthenticated requests to sources such as USGS,
NOAA, NASA, public RSS feeds, and GitHub's public API. These services can be
unavailable, rate-limited, or return changed schemas. Public access does not waive
the source's attribution, acceptable-use, or content-republication terms.

## Calendar Examples

Static calendar examples are keyless. Public ICS examples fetch public URLs.
Private calendars require credentials supplied through an execution profile;
never place private feed URLs or tokens in an exported graph.

## Worker Capabilities

Provider-backed and networked examples require a worker allowed to make the
documented outbound requests. Media workflows may also require managed artifact
storage. A future BYO worker may advertise a different capability set, so do not
assume every worker can execute every example.
