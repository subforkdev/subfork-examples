# OpenAI Speech Generation

This reference graph uses generic Subfork primitives to call OpenAI text-to-speech and return previewable audio media.

Before running it, add a graph-scoped secret named `OPENAI_API_KEY` in Graph Settings > Execution Profile.

The graph shape is:

`Text Value -> JSON Template -> HTTP Request -> Media Response`

`HTTP Request` now exposes `media` for `audio/*`, `image/*`, and `video/*` responses by wrapping bounded response bytes as a `data:` URL. That keeps this graph usable without a dedicated OpenAI node or artifact store.

Expected outputs:

- `audio` points at the speech request node's media output for Audio Preview panels.
- `response` points at `Audio Response` for API-style graph execution.

Known v0 caveat: inline `data:` URLs are fine for short local audio previews, but artifact storage should eventually replace large binary payloads.
