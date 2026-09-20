# OpenAI Asset Pack

This graph generates a coordinated image, voiceover audio clip, metadata JSON, and markdown campaign brief from one prompt/script pair.

Before running it, add a graph-scoped secret named `OPENAI_API_KEY` in Graph Settings > Execution Profile.

High-level shape:

```text
Creative prompt -> Image JSON body -> OpenAI image request -> Base64 image -> Image media
Voice script -> Speech JSON body -> OpenAI speech request -> Audio media
Image media + Audio media + Prompt + Script -> Metadata JSON -> Markdown campaign brief
Image media -> Media Response
Audio media -> Media Response
Markdown campaign brief -> Text Response
```

Recommended panels:

- Image Preview bound to `Image media: media`
- Audio Preview bound to `Speech request: media`
- Markdown Preview bound to `Campaign brief: value`
- JSON Inspector bound to `Asset metadata: value`

Why this graph exists:

- It exercises fan-out from authored inputs.
- It runs multiple provider requests in parallel once the executor supports async scheduling.
- It exercises image, audio, markdown, JSON, and media response panels together.
- It highlights the need for artifact storage because large inline `data:` URLs are useful locally but not ideal long term.
