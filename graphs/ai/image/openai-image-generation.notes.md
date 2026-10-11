# OpenAI Image Generation

![OpenAI Image Generation example thumbnail](openai-image-generation.thumbnail.jpg)

[Download graph](openai-image-generation.subfork.json)

This graph calls OpenAI image generation, previews the returned image, and also
passes its data URL through Image Resize to create a stored JPEG execution
artifact. Add a graph-scoped `OPENAI_API_KEY` secret before running it.

The `image` output is inline preview media. The `asset` output is an
artifact-backed 1024×1024 JPEG, suitable for downstream artifact-aware nodes.
It is still an execution output and expires under the normal artifact retention
policy. To keep it as an account asset, open the graph's Assets panel after the
run and retain the generated output. Retained outputs count against account
storage quotas.

The provider request may cost money. Re-running the graph creates another paid
image and another temporary execution artifact. No API key or generated image is
shipped in the export.
