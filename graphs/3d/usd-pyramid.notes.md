# USD Pyramid

Import `usd-pyramid.subfork.json` with recommended panels and Run. Text Value
contains a tiny self-contained ASCII USD mesh. USD ASCII Asset turns it into a
scene object, Transform / Motion supplies rotation, and Camera / Compose Scene
produce the same scene contract used by procedural examples. Choose Play in the
3D Preview header settings menu to rotate.

The asset travels with the graph in its Text Value node. The viewport does not
open files independently of the graph. Parser tests use a separate fixture in
`frontend/web/tests/fixtures/pyramid.usda`.

This tests static mesh preview, not full USD compatibility. Only bounded,
self-contained ASCII USDA is enabled. Binary USD/USDC, USDZ, external references,
textures, variants, USD animation and Alembic are not supported yet. Applying
graph-authored motion to this static mesh is not USD animation-cache playback.

See [format support and limits](https://github.com/subforkdev/subfork-new/blob/master/docs/planning/subfork-3d-preview.md).
