# Cut Timeline Renderer

<a href="cut-timeline-renderer.subfork.json" download="cut-timeline-renderer.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Upload two video files of at least three seconds each and one audio file of at least six seconds, then run the graph. JSON Template preserves the three structured artifact references inside a declarative timeline. Media Timeline Render stages only those execution-authorized artifacts and produces one 1280×720, 30 fps, six-second MP4 with two hard cuts and the uploaded soundtrack.

This graph uses the released `n_media_timeline_render` node and requires artifact storage plus a worker advertising `media-worker`. It makes no external network requests and invokes no paid provider. Rendering consumes media-worker CPU, temporary disk, and account artifact quota. The example accepts source files up to 250 MB each, stages at most 500 MB in total, limits output to 100 MB, and times out after 300 seconds; lower account limits still apply.

Version 1 is intentionally cut-only. It scales and pads each clip without stretching, encodes H.264/AAC, and does not accept arbitrary FFmpeg options. Transitions, captions, overlays, and beat-driven clip assignment belong in later typed timeline fields or graph-backed composites.

Recommended panels: Video Preview for `video`, JSON Inspector for `render_info` and `timeline`, and Activity/Logs.
