# OpenAI Video Generation Job

This experimental graph submits an OpenAI video generation job and polls its status using generic Subfork job primitives.

Before running it, add a graph-scoped secret named `OPENAI_API_KEY` in Graph Settings > Execution Profile.

The graph shape is:

`Text Value + optional URL Input -> JSON Template -> HTTP Submit Job -> JSON Path -> Status URL -> HTTP Poll Job -> Content URL -> HTTP Request -> Video Preview`

The composite surface should expose:

- `prompt`: required text prompt.
- `image_url`: optional image reference. This may be a fully qualified image URL or a base64-encoded `data:image/...` URL.

For an uploaded reference image, add an `Image Asset` node and connect its `url`
output to `image_url`. Provider URL handoff requires a publicly reachable Subfork
deployment; `subfork.localhost` cannot be fetched by OpenAI.

The `Status URL` node constructs `/v1/videos/{id}` from the submitted job ID. After the poll node reaches `completed`, `Video content URL` constructs `/v1/videos/{id}/content`, and `Fetch video content` retrieves the authenticated video bytes as a `video/*` media payload for the Video Preview panel.

The request body uses JSON Template optional keys:

```json
{
  "input_reference?": {
    "image_url?": "{{ inputs.image_url }}"
  }
}
```

The trailing `?` means "omit this key when the rendered value is empty, null, an empty array, or an empty object." That prevents invalid payloads such as `"image_url": ""` when the graph is used text-only.

Expected outputs:

- `job` is the submitted remote job reference.
- `status` is the current video job status.
- `response` is the latest job JSON response.
- `video` is the downloaded video content media payload.

Known v0 caveats:

- OpenAI video generation is a long-running job API, so this graph depends on Subfork's async worker/resume execution.
- Downloaded video is stored as a managed execution artifact and passed through the graph by reference.
- The OpenAI video API is marked deprecated in current API docs and is scheduled to shut down on September 24, 2026, so keep this as an experimental compatibility template.
