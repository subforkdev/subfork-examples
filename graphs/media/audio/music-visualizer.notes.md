# Music Visualizer

<a href="music-visualizer.subfork.json" download="music-visualizer.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Upload an audio file, inspect it with **Media Probe** on a capability-routed media worker, and open a beat-reactive browser visualization. Graph nodes configure the initial visualization, beat sensitivity, accent color, and secondary color. The responsive HTML preview fills its panel and offers six live styles: radial spectrum, block equalizer, dot spectrum, layered ribbons, waveform field, and console.

## Try It

1. Import the graph into Subfork.
2. Upload an MP3, WAV, M4A, Ogg, or another format supported by its FFmpeg build.
3. Run the graph and confirm **Probe audio on media worker** completes.
4. Open the recommended HTML Preview and use the icon button beside **Pulse Canvas** to play or pause. Choose **Radial**, **Blocks**, **Dots**, **Ribbons**, **Wave**, or **Console** from the compact style switcher. Play starts Web Audio analysis; browsers require this user gesture before playback and analysis begin.
5. Inspect `probe_info` in the JSON panel. It should report the container, codec, duration, sample rate, and channel count.

The execution path is `Asset + visualization controls → Media Probe → JSON Template → JSON Stringify → HTML Template → HTML Response`. Text, Range, and Color input nodes define the initial visual state. JSON Template combines those controls with the durable artifact reference and probe result, and JSON Stringify safely embeds that page-data object in the HTML. The `visualizer_config` graph output exposes the resolved page data for inspection and reuse. Media Probe reads at most 50 MB through an execution-scoped artifact grant, invokes `ffprobe` with a 15-second timeout and bounded diagnostic output, and requires the `media-worker` worker capability. With the default plan map, administrators and paid accounts may run it; free accounts receive an entitlement error before launch. There are no provider credentials, paid API calls, or third-party network requests.

The visualization runs locally in the rendered page. The graph controls configure the initial renderer state, while a Web Audio analyser and moving bass-energy threshold calculate live motion in the browser. The preview only exposes playback and style selection; sensitivity and colors remain graph-authored controls. This is not server-side beat detection and does not produce a video file. Music Analysis can expose reusable beat, envelope, and spectral data for rendered-video and non-browser composites. HTML Preview asks its authenticated workspace host to resolve the typed artifact reference into a browser-local Blob URL. The graph and generated HTML contain no signed URL, and historical previews continue to work while the execution and asset are retained and authorized.

This example targets the released `n_media_probe` 1.0.0 node and is marked `media-worker-probe`. Repository validation covers its graph structure and released node contract. A fresh import, media-worker routing, MP3/WAV playback, and browser rendering remain manual checks.
