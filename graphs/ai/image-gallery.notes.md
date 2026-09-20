# AI Image Gallery

## What This Template Proves

This probes capability-oriented AI nodes and graph-scoped execution profiles for provider credentials.

## Current Behavior

The graph imports and runs today, but it only returns prompt records. No provider call is made.

## Faked Pieces

- This seed does not generate images. Separate OpenAI image-generation seeds
  exist; this fixture has not been wired to those provider calls.
- Mapping over prompt collections is not implemented.
- Gallery panel is not implemented.
- Provider/model selection is only represented in notes and template requirements.

## Missing Nodes And Panels

- Generate Image node
- Map / For Each node
- Gallery panel accepting `Collection<ImageAsset>`
- Asset reference type for generated images
- Bind the existing graph-scoped execution profile secrets to provider calls

## Architecture Implications

Provider selection should be node configuration or execution-profile-backed settings, while API keys are stored as graph-scoped secrets outside graph definitions, exports, and forks.
