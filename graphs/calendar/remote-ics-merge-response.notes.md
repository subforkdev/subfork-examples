# Remote ICS Merge Response

## What This Template Proves

This is the first end-to-end calendar feed probe: public URL inputs, HTTP fetch, ICS parse, merge, sort, and `text/calendar` graph response.

## Current Behavior

The graph imports and runs when the worker can reach the public calendar hosts.
The authoring `/execute` path records execution and exposes the response object
for inspection, including its `text/calendar` body. Direct `/graphs/:id/response`
delivery is disabled (503); a subscription URL is not currently available.

## Faked Pieces

- The feeds are public examples, not graph-scoped private calendar credentials.
- There is no recurrence expansion yet.
- Timezone handling is intentionally shallow in this first parser.
- The authoring UI does not yet provide a one-click copied subscription URL.

## Next Wiring Step

Add an authenticated or publishable run URL with access-control policy, quota, and execution-profile selection. Private calendar URLs and tokens should resolve from the graph-scoped execution profile, not from exported graph JSON.
