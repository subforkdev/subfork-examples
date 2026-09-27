# Music Beat Grid

<a href="music-beat-grid.subfork.json" download="music-beat-grid.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Upload an audio file and run the graph to inspect a reusable beat grid, normalized energy envelope, estimated tempo, and edit windows. The example analyzes at most the first 30 seconds and asks Edit Windows for complete coverage of the first 15 seconds, with cuts preferably aligned to estimated downbeats.

This graph uses the released `n_music_analysis` and `n_edit_windows` nodes. Music Analysis requires a `media-worker` worker and reads no more than 50 MB. Edit Windows is deterministic JSON processing on ordinary worker capacity. Neither node makes an external network request or invokes a paid provider.

Beat and downbeat detection is an initial deterministic estimate. Downbeats assume groups of four beginning with the first detected beat. Quiet, ambient, rubato, or highly syncopated tracks may produce sparse or inaccurate timing; inspect the JSON result before using it for a render.

Recommended panels: JSON Inspector for `analysis` and `edit_windows`, Audio Preview for `audio`, and Activity/Logs.
