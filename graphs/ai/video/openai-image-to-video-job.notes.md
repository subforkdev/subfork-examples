# OpenAI Image to Video Job

[Download graph](openai-image-to-video-job.subfork.json)

Upload a reference image, fit it to a supported video resolution, and submit an
OpenAI video job. This remains an experimental compatibility example built from
generic artifact, image, HTTP job, and polling nodes.

## Try it

1. Import the graph and add the graph-scoped `OPENAI_API_KEY` secret.
2. Upload or select a PNG, JPEG, or WebP in **Reference image**.
3. Set **Video size** to a resolution supported by the selected model. The same
   value configures the resize operation and provider request.
4. In **Fit reference image**, choose `pad` to preserve the whole image with
   borders or `crop` for a centered crop. Neither mode stretches the image.
5. Edit the prompt and run. Inspect the JSON response and open Video Preview for
   the retained result.

**Create provider image URL** explicitly converts the resized artifact into an
externally fetchable URL. Private artifacts receive a fresh signed URL with a
15-minute TTL; public artifacts use their stable public route. URL minting uses
the node attempt's scoped artifact grant, so the worker does not receive signing
credentials or access to unrelated artifacts. Re-running the graph creates a
fresh URL without duplicating the uploaded source image.

The signed URL is sent to OpenAI and remains in the execution record after it
expires. It is intended for the provider request made by that execution, not as a
durable graph value or published link.

## Network, limits, and effects

Image Resize reads the source through Subfork's scoped artifact delivery and
writes a new execution-output artifact. Inputs are limited to 8192 pixels per side
and 20 megapixels. Outputs are limited to 4096 pixels per side, 8 megapixels, and
5,000,000 bytes. The node rejects animated images, applies EXIF orientation,
flattens transparency onto the chosen background, and produces JPEG at quality
85. The original upload is unchanged.

Resizing is deterministic and makes no provider call. The prompt, resized image
URL, and generation settings are sent to OpenAI. Submission may create a billable
remote job. Polling and download use the limits documented by the base
[OpenAI Video Generation Job](openai-video-generation-job.notes.md). Repeating
execution can create another billable job. The downloaded video is retained as an
execution artifact; this graph does not publish or delete media.

No URL, credential, artifact ID, uploaded file, or generated media is shipped in
the export.
