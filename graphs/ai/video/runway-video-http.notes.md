# Runway Video HTTP

![Runway Video HTTP example thumbnail](runway-video-http.thumbnail.jpg)

A reusable Gen-4.5 video-task submission graph built entirely from generic
Subfork nodes. It contains no environment-specific graph IDs, composite
references, credentials, or generated media. Import it independently, or publish
it as a composite before building higher-level video workflows.

## Inputs and outputs

| Input | Type | Meaning |
| --- | --- | --- |
| `prompt` | `str` | Required description of the video |
| `image_url` | `url` | Optional public HTTPS first-frame image; absent or empty selects text-to-video |
| `duration` | `int` | Defaults to 5 seconds; provider supports integers from 2–10 |
| `ratio` | `str` | Defaults to `1280:720`; `720:1280` also works in both modes |

Outputs are `job` (resumable job reference), `task_url` (typed polling URL),
`task_id`, and `submission_response` (raw provider submission JSON).
**This graph submits a task; it does not wait for or return the finished video.**

Configure `RUNWAYML_API_SECRET` in **Graph Settings → Execution Profile** on the
executing graph. When used as a composite, the executing parent owns the secret;
publication does not distribute credentials. Supply graph inputs through the
Python/API execution interface, or connect inputs on the published composite.

## HTTP behavior and cost

The graph sends one paid POST to the fixed origin `https://api.dev.runwayml.com`:

- `/v1/text_to_video` when `image_url` is absent or empty;
- `/v1/image_to_video` when an image is supplied.

Both requests use model `gen4.5`, bearer authentication, and
`X-Runway-Version: 2024-11-06`. The endpoint choice is restricted to these two
paths; callers cannot replace the credential-bearing origin. The job node uses
runtime HTTP defaults of a 30-second timeout and 1,000,000 response bytes.
Image URLs must be reachable by Runway and return an accepted image without
redirects. Localhost and local file paths are not suitable. The provider validates
prompt lengths, image constraints, duration, aspect ratio, and account limits.

Every execution can consume provider credits and Subfork quota. If a submission
has an uncertain outcome, inspect the existing execution/task before trying
again; automatic resubmission can create another paid generation.

## Compose a complete video graph

After importing, validate and publish the adapter as `v0.2.1` (or a deliberately
chosen new version for changed content). Obtain the generated composite node
manifest from the **target instance**. Build a parent with:

1. Editable prompt and ratio controls connected to the composite; optionally
   bind its `image_url` and `duration` inputs.
2. `job` connected to HTTP Poll Job's `remote_job` input.
3. `task_url` connected to the poll node's exposed `status_url` input.
4. Poll `media` connected to Media Response or a Video Preview panel.

Use these poll parameters:

```json
{
  "headers": {
    "Authorization": "Bearer {{ secrets.RUNWAYML_API_SECRET }}",
    "X-Runway-Version": "2024-11-06"
  },
  "status_path": "status",
  "complete_values": ["SUCCEEDED"],
  "failed_values": ["FAILED", "CANCELED", "CANCELLED"],
  "media_url_path": "output.0",
  "poll_after_seconds": 10,
  "max_attempts": 180,
  "max_elapsed_seconds": 1800
}
```

Expose `status`, raw task `response`, and video `media` from the parent.
The runtime normalizes the status to lowercase. Poll failures stop the graph.
Exhausting polling bounds does not cancel the provider task. Runway's output
URLs expire in 24–48 hours: download videos to lasting storage separately, using
an unauthenticated request to the media URL, not the Runway authorization header.

Keep polling at the top level. In the tested development runtime, a composite
containing a waiting child lost child resume state and repeated the submission.
The submission-only adapter completes once; the parent then resumes just its
poll node. Do not nest the complete asynchronous parent inside another composite
until that runtime limitation is addressed.

## Recreating parents on another instance

A raw parent export containing a development graph ID is not portable. For now:

1. Import and publish this leaf on the target instance.
2. Record a tooling-level mapping from logical adapter name to target graph ID
   and exact published version.
3. Use the target publication's manifest to fill the parent's composite `node_id`,
   `node_version`, and `params.composite_graph` reference.
4. Validate the assembled parent before publishing or executing it. Configure
   target-owned secrets separately.

Pin the reviewed version. Graph IDs differ between environments, but the same
reviewed release can retain the label `v0.2.1`. An existing version with different
content must not be silently reused or overwritten. A missing version should
produce an installation error, not a fallback to `latest`.

Publisher-scoped slugs and portable references are proposed features, not current
graph fields. They can eventually identify the adapter independently of its
local graph ID while retaining exact-version pins. A slug still needs the
intended publisher/catalog and the requested release installed on the target.
This example deliberately does not introduce unsupported reference fields or
ship parent graphs with development IDs.

## Validation status

The v0.2.1 source adapter and prompt-only parent were validated and published on
development. One five-second prompt-only generation completed on 2026-10-10;
the returned MP4 was readable and the user confirmed Video Preview playback.
Seven mocked runtime tests covered omitted, empty, and present image inputs,
endpoint selection, single submission across polling resumes, failure and
cancellation, missing task ID, and polling limits.

This portable export is checked against production node contracts. It has not
been freshly imported and executed on production. Live image-to-video generation
remains untested. Catalog validation is not evidence of production provider
execution. No additional paid generation was performed when adding this example.

The endpoint split follows Runway's official
[text-to-video schema](https://github.com/runwayml/sdk-python/blob/main/src/runwayml/types/text_to_video_create_params.py)
and [image-to-video schema](https://github.com/runwayml/sdk-python/blob/main/src/runwayml/types/image_to_video_create_params.py).
See also [input requirements](https://docs.dev.runwayml.com/assets/inputs/) and
[output lifetime](https://docs.dev.runwayml.com/assets/outputs/). A getting-started
example that suggested omitting the image on the image-to-video endpoint did not
match the observed API behavior; that request returned HTTP 400.
