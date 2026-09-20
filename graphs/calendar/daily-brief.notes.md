# Daily Calendar Brief

## What This Template Proves

This probes ICS parsing, event merging, date filtering, sorting, and future calendar visualization.

## Current Behavior

The graph imports and runs today using embedded mock ICS text. It parses work and personal calendars, merges the event lists, returns events for `2026-09-01`, and sorts them by `start`.

## Faked Pieces

- Provider fetching is mocked with static ICS text nodes.
- Date filtering uses explicit ISO date parameters rather than relative ranges like `today`.
- Calendar rendering and natural-language brief generation are not implemented.

## Missing Nodes And Panels

- Optional provider-specific Calendar Fetch nodes
- Event Normalize node for richer provider and timezone behavior
- Date/Time Filter node with relative dates
- Calendar panel accepting `Collection<Event>`
- Optional Summarize/Template Render node

## Architecture Implications

Calendar providers need graph-scoped execution profile secrets. Forking or publishing should carry the event workflow, not the user’s provider token.
