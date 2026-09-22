# Natural Event Keyword Router

<a href="../natural-event-keyword-router.subfork.json" download="natural-event-keyword-router.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Demonstrates the decision core of an IFTTT-style graph: fetch a bounded public
event snapshot, test a condition, and choose one of two routing values. It checks
the raw JSON from ten recent open NASA EONET events for the `wildfires` category.

Running the graph is the trigger. The `decision` JSON is an action placeholder;
the graph has no schedule, subscription, webhook trigger, notification, or
external write. Subfork's Conditional node selects a value but does not suppress
execution of downstream branches, so side-effecting actions should not be wired
as if this were control-flow gating.

The request is keyless and read-only, limited to ten events from the previous 30
days, with a 20-second timeout and 500 KB response cap. Expected outputs are
`matched`, `decision`, provider `status`, and a JSON `response`. Category matches
depend on the bounded snapshot and are not an emergency alert.

Source: [NASA EONET API v3](https://eonet.gsfc.nasa.gov/docs/v3). No external
action was executed while authoring or validating this example.
