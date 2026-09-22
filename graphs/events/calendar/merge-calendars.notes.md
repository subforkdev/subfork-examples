# Merge Calendars

## What This Template Proves

This probes the basic calendar pipeline shape: parse separate iCalendar sources, merge event lists, sort chronologically, and return table-ready JSON.

## Current Behavior

The graph imports and runs using embedded mock ICS strings. It returns normalized event rows with fields like `uid`, `title`, `date`, `start`, `start_time`, `end`, `location`, and `url` when present.

## Faked Pieces

- Live calendar fetching is represented by static ICS text nodes.
- Private calendar credentials are not stored in the graph.
- Calendar, table, and Gantt widgets are not automatically opened or bound by the template yet.

## Next Wiring Step

Replace each static ICS node with `URL Input -> HTTP Request -> ICS Parse` for public feeds. Private feeds should resolve credentials from the graph-scoped execution profile once secure storage lands.
