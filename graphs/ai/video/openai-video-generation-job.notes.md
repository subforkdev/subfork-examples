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

## Troubleshooting rejected requests

- **Incorrect API key provided:** OpenAI rejected the credential. Re-enter the
  intended API key as the graph-scoped `OPENAI_API_KEY` secret in Graph Settings >
  Execution Profile, then rerun. The export contains only the secret reference.
- **Inpaint image must match the requested width and height:** the reference
  image must have exactly the resolution in **Video size (width x height)**. This
  example requests `1280x720`; use an image resized/cropped to those dimensions,
  or omit the optional image input for a text-only test. Matching the aspect ratio
  alone is insufficient. The graph does not resize images automatically.
- **JSON Path could not resolve 'id':** on older runtimes, an unsuccessful submit
  could pass the provider's error object to **Video id**. That object has no job
  ID. Inspect **Submit video job → response** for the original provider error.
  This is a caught node failure, not an unhandled application exception.

With the updated HTTP job runtime, submit and poll nodes fail on non-2xx HTTP
responses and surface the provider's message at the originating node. The JSON
response remains available for inspection. A successful submit must contain the
configured job ID; a poll must contain its configured status. Missing fields stop
execution instead of causing a later JSON Path error or repeated empty polls.
Update the API/worker runtime to get this behavior; the existing graph wiring
can stay as it is. Rejected requests are not retried automatically.

Video generation calls may cost money. Fix the input before rerunning: a new
submission may create a new billable remote job. The submit request uses the
HTTP node defaults of 30 seconds and 1,000,000 response bytes; polling uses the
same request bounds and defaults to at most 120 polls or 3600 elapsed seconds.
Video downloads are capped at 120 seconds and 25,000,000 bytes. Media is stored as
an execution artifact; this graph does not publish or delete the resulting video.

[OpenAI reference-image requirements](https://developers.openai.com/api/docs/guides/video-generation#use-image-references)

For automatic reference-image fitting, import [OpenAI Image to Video Job](openai-image-to-video-job.notes.md). Its shared size input drives both Image Resize and the video request. This base example keeps the image input optional and does not resize it.
