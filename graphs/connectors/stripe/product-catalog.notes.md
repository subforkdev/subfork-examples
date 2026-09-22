# Stripe Product Catalog

<a href="../product-catalog.subfork.json" download="product-catalog.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Reads the first ten active products from a Stripe account.

Before running, create a Stripe restricted API key with read access to Products
and add it as the graph-scoped execution-profile secret
`STRIPE_RESTRICTED_KEY`. Start with a test-mode key. Do not put the key in the
graph document, a URL, or a regular execution-profile variable.

The graph calls Stripe's fixed `GET /v1/products` endpoint with `active=true` and
`limit=10`. It uses a 20-second timeout and a 500 KB response cap. It does not
follow pagination, create or modify products, retrieve prices, or read customer
and payment data. The fixed provider URL prevents composite callers from routing
the credential to another host.

Expected outputs are `products`, provider `status`, and a JSON `response`. Bind
`products` to a Table panel. Stripe API availability, rate limits, and account
terms apply. No live Stripe request was made while authoring this example.

Provider references: [list all products](https://docs.stripe.com/api/products/list)
and [API authentication](https://docs.stripe.com/api/authentication).
