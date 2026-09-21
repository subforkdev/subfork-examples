# OpenAI 3D Generation

We do not have a working OpenAI 3D generation graph template yet.

Current gaps:

- The local panel registry has Image Preview, Audio Preview, Video Preview, JSON, HTML, Table, Logs, and Artifact Inspector, but no 3D viewer panel.
- The current OpenAI API model catalog does not expose a dedicated 3D asset generation endpoint in the same way it exposes image, speech, transcription, realtime, and video endpoints.
- A useful 3D path probably needs a new media/artifact type for meshes or scenes, plus a Three.js-style preview panel that can render `model/gltf+json`, `model/gltf-binary`, OBJ, USDZ, or similar asset references.

Suggested direction:

Author 3D-capable graphs around generic artifact/media primitives first, then add a `3D Preview` panel once we have a concrete provider or file format to target.
