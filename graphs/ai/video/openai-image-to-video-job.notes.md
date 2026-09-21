# OpenAI Image to Video Job

<a href="../openai-image-to-video-job.subfork.json" download="openai-image-to-video-job.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Upload an image, fit it to the requested video resolution, and generate a short
video. This extends [OpenAI Video Generation Job](openai-video-generation-job.notes.md)
with Image Asset metadata and Image Resize. The underlying video API is experimental;
review the base example's provider availability and troubleshooting notes.

## Try it

1. Update the API, frontend, node catalog, and workers with Image Resize support.
   The runtime now requires Pillow. Rebuild the relevant dev images.
2. Import and save this graph. Add the graph-scoped secret `OPENAI_API_KEY` in
   Graph Settings > Execution Profile.
3. Select **Upload reference image** and upload a still PNG, JPEG, or WebP. The
   canvas thumbnail appears immediately when **show thumbnail** is enabled.
4. Set **Video size (width x height)**, default `1280x720`. This one value feeds
   both the resize node and the OpenAI request. Use a resolution supported by
   the selected video model; `720x1280` is the portrait counterpart.
5. In **Fit reference image to video**, choose `pad` to preserve the whole image
   with borders, or `crop` for a centered crop that fills the frame. `pad` with a
   black background is the default. Neither mode stretches the image.
6. Edit the prompt and run. Image Preview shows the fitted reference; Video
   Preview shows the downloaded video when the job completes. The image preview
   is an output, not an approval gate: submission proceeds automatically.

The `info` port reports width, height, size, aspect ratio, and format. Image Asset
reports dimensions after accounting for EXIF orientation. Older uploads without
stored metadata return an empty info object; reupload to populate it. Image Resize
always reports output dimensions and the source dimensions it actually decoded.

## Network, limits, and effects

Image Resize reads the signed image URL using bounded public HTTP (30 seconds,
5,000,000 bytes, no redirects or private/local destinations). Your instance or
artifact storage must be publicly reachable. It also accepts small base64 image
URLs when used outside this example.

Inputs are limited to 8192 pixels per side and 20 megapixels. Outputs are limited
to 4096 pixels per side, 8 megapixels, and 5,000,000 bytes. The node rejects animated
images, applies EXIF orientation, flattens transparency onto the chosen background,
and produces JPEG at quality 85. The original upload is unchanged. The resized
image is a new execution artifact, with a temporary signed provider URL. Small
standalone executions without an artifact writer can return inline JPEG instead;
outputs above 250,000 bytes require artifact storage with provider URL support.

Resizing is deterministic and makes no AI-provider call. The subsequent video
submission and polling have the same paid provider requirements, timeouts, download
caps, and remote-job side effects as the base example. The resized image, prompt,
and generation settings are sent to OpenAI. Repeating execution can create another
billable video job. This graph does not publish or delete media.

No uploads, artifact IDs, signed URLs, credentials, or generated media are shipped
in the export. Upload your own image after import. The exported artifact ID is empty.

[OpenAI image-reference requirements](https://developers.openai.com/api/docs/guides/video-generation#use-image-references)
