# Open Tickets Pipe

## What This Template Proves

This is the smallest runnable row-processing pipeline: JSON rows flow through filter, sort, limit, and response nodes.

## Current Behavior

The graph imports and runs today. It returns open tickets sorted by descending priority and limited to two rows.

## Faked Pieces

The ticket data is static. A real template would likely fetch from a provider-backed issue tracker, table service, or database.

## Missing Nodes And Panels

- Provider-backed data query node
- More expressive filter predicates
- Table panel binding as template metadata
- Optional execution profile connection selection

## Architecture Implications

Generic data nodes should support operation configuration, while credentials and connection settings come from graph-scoped execution profiles.
