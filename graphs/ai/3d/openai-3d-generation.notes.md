# OpenAI 3D Generation

![OpenAI 3D Generation example thumbnail](openai-3d-generation.thumbnail.jpg)

We do not have a working OpenAI 3D generation graph template yet.

Current gaps:

- The local panel registry has Image Preview, Audio Preview, Video Preview, JSON, HTML, Table, Logs, and Artifact Inspector, but no 3D viewer panel.
- OpenAI shut down its Videos API and Sora 2 models on September 24, 2026, and lists no replacement. OpenAI therefore has no currently available video-generation endpoint for this pipeline; use another provider for video generation.
- A useful 3D path probably needs a new media/artifact type for meshes or scenes, plus a Three.js-style preview panel that can render `model/gltf+json`, `model/gltf-binary`, OBJ, USDZ, or similar asset references.

Suggested direction:

Author 3D-capable graphs around generic artifact/media primitives first, then add a `3D Preview` panel once we have a concrete provider or file format to target.
