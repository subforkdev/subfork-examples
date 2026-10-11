# OpenAI Speech Generation

![OpenAI Speech Generation example thumbnail](openai-speech-generation.thumbnail.jpg)

[Download graph](openai-speech-generation.subfork.json)

This reference graph uses generic Subfork primitives to call OpenAI text-to-speech
and return previewable audio. Add a graph-scoped `OPENAI_API_KEY` secret before
running it.

The HTTP Request node explicitly sets `response_storage` to `artifact`, so a
successful audio response is stored as a temporary execution artifact even if its
artifact output is not connected to another node. The graph exposes that artifact
as `asset`. To keep it as an account asset beyond execution-artifact expiry,
retain the generated output from the graph's Assets panel. Retained outputs count
against account storage quotas.

Provider calls may cost money. Re-running the graph creates a new paid speech
request and a new temporary artifact.
