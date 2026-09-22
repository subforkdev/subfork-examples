# Slack Webhook Message

<a href="../webhook-message.subfork.json" download="webhook-message.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Posts one message to the channel associated with a Slack incoming webhook.

Before running, create or select a Slack app with incoming webhooks enabled and
add the complete webhook URL as the graph-scoped secret `SLACK_WEBHOOK_URL`.
Webhook URLs are credentials: never paste one into the graph, export, notes, or
logs. Edit **Message to send**, review the destination channel, and run once.

**This graph performs an externally visible write.** Every successful execution
posts a new Slack message. Re-running after an ambiguous timeout can duplicate the
message, and incoming webhooks cannot delete messages they posted. The request has
a 20-second timeout and a 64 KB response cap. Slack normally returns plain-text
`ok`; errors may use other HTTP statuses and text bodies.

Expected outputs are provider `status`, `provider_response`, and a text `response`.
Slack service terms and workspace policies apply. No live webhook request was made
while authoring or validating this example.
