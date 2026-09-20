# OpenAI Image Generation

This reference graph tests provider-backed image generation using generic Subfork primitives rather than a hardcoded provider node.

Before running it, add a graph-scoped secret named `OPENAI_API_KEY` in Graph Settings > Execution Profile.

The only user-editable content required for a basic run is the `Editable prompt` node. Change its `text` parameter to change the generated image prompt.

The graph shape is:

`Text Value -> JSON Template -> HTTP Request -> JSON Path -> Base64 Image To Media -> Media Response`

`JSON Template` exposes a custom `prompt` input and renders it into the request body with `{{ inputs.prompt }}`. This graph is intended to become a candidate composite/subgraph node later: the authoring view can show the internals, while the higher-level graph can show a single `OpenAI Image Generation` node with `prompt` in and `image` out.

Expected outputs:

- `image` points at the `Image media` node's media output for Image Preview panels.
- `response` points at `Media Response` for API-style graph execution.

Known v0 caveat: the response envelope redirects to the generated media URL. For base64 image data this is currently a `data:` URL, which is useful for local preview. Future artifact storage should replace large inline data URLs with artifact references.

The request body intentionally asks for a smaller response payload:

```json
{
  "size": "1024x1024",
  "quality": "low",
  "output_format": "jpeg",
  "output_compression": 70
}
```

`gpt-image-1` does not currently expose smaller fixed dimensions than `1024x1024`, so compressed JPEG/WebP output is the practical v0 way to reduce the base64 JSON response size.
