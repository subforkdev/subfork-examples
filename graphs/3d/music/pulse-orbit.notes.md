# Pulse Orbit

[Download graph](pulse-orbit.subfork.json)

Upload an audio file and run the graph. The graph analyzes at most the first 30 seconds and 50 MB. Music Analysis runs on a `media-worker`; the shaping and scene nodes use ordinary worker capacity. There are no network calls, credentials, paid providers, generated media, or externally visible side effects.

This graph demonstrates the intended composite design for music-driven motion. JSON Path selects the 20 Hz normalized energy envelope and detected downbeats. Compute Field turns energy into vertical offset and uniform scale, while another branch turns downbeat indices into yaw angles. Map / Project Fields shapes ordinary rows into translation, rotation, and scale records. Two Scene TRS Keyframes nodes produce reusable animation documents, and two nested Transform / Motion nodes apply the pulse and turn tracks to one sculpture.

The scene uses a right-handed Y-up coordinate system in arbitrary scene units. A sphere sits at the origin, surrounded by eight instanced boxes at radius 3. Energy maps from 0–1 to Y offsets from -0.35–0.35 and scale multipliers from 1–1.65. Each detected group of four beats advances the sculpture by 0.4 radians with step interpolation. The scene duration and analysis window are both 30 seconds.

Audio Preview and 3D Preview currently have separate browser playback clocks. Start them together for an approximate preview; this example does not claim frame-accurate audio synchronization. Quiet, ambient, rubato, or highly syncopated tracks may yield no downbeats or inaccurate timing. If analysis returns no downbeats, the downbeat keyframe branch rejects the empty list; inspect `analysis` and try a track with a clear pulse.

This first example keeps the scene graph-owned and procedural. It does not upload a USD asset: Asset produces a durable artifact reference, while USD ASCII Asset currently accepts UTF-8 text. A future artifact-to-scene-data path can replace the sculpture without changing the analysis-to-keyframes composite.

This graph uses the released `n_music_analysis` and `n_scene_keyframes` contracts and requires a worker advertising `media-worker` for audio analysis. Recommended panels: 3D Preview for `scene`, Audio Preview for `audio`, JSON Inspector for `analysis`, and Activity/Logs.
