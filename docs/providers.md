# Provider Requirements

Most examples are keyless, but the repository also includes account-backed and
potentially billable provider integrations. Always inspect the companion notes
before running one. Provider plans, prices, quotas, and terms can change
independently of Subfork.

Keep credentials in graph-scoped execution-profile secrets. The names below are
part of each example's contract; never place the underlying value in graph JSON,
a URL, notes, logs, or a regular variable.

## OpenAI

The runnable OpenAI examples require a graph-scoped secret named
`OPENAI_API_KEY`. Configure it in Graph Settings under the execution profile.
The key is resolved by the worker and must never appear in graph JSON.

Image, speech, Responses API, asset-pack, and video operations can incur usage
charges. Some graphs make more than one paid request per execution, and a retry
can incur the charges again. Video jobs are long-running and their provider API
may change or be retired. PDF narration sends the prompt and a temporary signed
file URL to OpenAI. Consult the individual example's notes and current provider
documentation before use.

## Airtable

[Airtable Record Browser](../graphs/connectors/airtable/record-browser.notes.md)
requires:

- graph variables `AIRTABLE_BASE_ID` and `AIRTABLE_TABLE_ID`;
- graph secret `AIRTABLE_ACCESS_TOKEN`, restricted to read-only record access
  for the required base.

The example reads at most 25 records and does not follow pagination or perform
writes. Airtable plan limits, API quotas, and account terms apply. Execution
outputs may contain data from the configured base.

## Stripe

[Stripe Product Catalog](../graphs/connectors/stripe/product-catalog.notes.md)
requires the graph secret `STRIPE_RESTRICTED_KEY`. Use a restricted key with
read access to Products and start in test mode.

The example lists at most ten active products. It does not create or modify
products, retrieve prices, or access customer and payment data. The read itself
is not a payment operation, but Stripe account restrictions, API limits, and
service terms still apply.

## Supabase

[Supabase Table Reader](../graphs/connectors/supabase/table-reader.notes.md)
requires the graph secret `SUPABASE_PUBLISHABLE_KEY` and a reviewed project and
relation in the fixed request URL. Use a publishable key; never substitute a
secret or service-role key.

The example reads at most 25 rows and performs no writes. Row Level Security is
responsible for limiting which rows and columns the key may read. Supabase plan,
database, bandwidth, and API limits apply, and execution outputs may contain all
columns returned by the configured relation.

## Slack

[Slack Webhook Message](../graphs/connectors/slack/webhook-message.notes.md)
requires the graph secret `SLACK_WEBHOOK_URL`.

This example performs an externally visible write: every successful execution
posts a message to the webhook's channel. Retrying after an ambiguous timeout
can create a duplicate, and the webhook cannot delete messages it posted. Slack
workspace policies, plan limits, and service terms apply.

## GitHub And Google Sheets

[Public GitHub Releases](../graphs/connectors/github/public-releases.notes.md)
is keyless and read-only. Unauthenticated GitHub requests have lower rate limits,
and the example reads only the first ten releases.

[Published Google Sheet](../graphs/connectors/google/published-sheet.notes.md) is
also keyless and read-only. It requires a sheet that its owner has explicitly
published to the web. Publishing can make the sheet broadly accessible, so do
not use this example for private or sensitive data.

## Public Data Sources

Several examples make bounded, unauthenticated requests to sources such as USGS,
NOAA, NASA, Open-Meteo, the World Bank, public RSS feeds, and government sensor
feeds. These services can be
unavailable, rate-limited, or return changed schemas. Public access does not waive
the source's attribution, acceptable-use, or content-republication terms.

## Calendar Examples

Static calendar examples are keyless. Public ICS examples fetch public URLs.
Private calendars require credentials supplied through an execution profile;
never place private feed URLs or tokens in an exported graph.

## Worker Capabilities

Provider-backed and networked examples require a worker allowed to make the
documented outbound requests. Media workflows may also require managed artifact
storage. A future BYO worker may advertise a different capability set, so do not
assume every worker can execute every example.
