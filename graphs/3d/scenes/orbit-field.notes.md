# Orbit Field

Import `orbit-field.subfork.json` with recommended panels, then Run. The 3D
Preview binds to Compose Scene's `scene` output. Rebuild API/workers/frontend
first for the new Scene nodes and panel type.

Three seeded integer lists feed Zip Lists, then point geometry and material.
Transform / Motion scales and rotates the point cloud. A separately authored
sphere/material joins it in a group, then Camera and Compose Scene produce JSON.

Drag to orbit, right-drag to pan, scroll to zoom. Choose Play in the panel settings menu for browser-local
motion; Reset returns to time zero. Frame scene and Authored camera change only
the viewer, not graph data. Edit seeds, count, materials or motion and Run again.

This is intentionally a simple point-field composition, not a fluid simulation.
Every scene element is graph-owned; there are no demo-specific renderer branches,
embedded scripts, external assets or credentials. Playback is not graph execution.
The output is scene JSON requiring a compatible renderer, not standalone HTML.

See [3D contract](https://github.com/subforkdev/subfork-new/blob/master/docs/planning/subfork-3d-preview.md).
