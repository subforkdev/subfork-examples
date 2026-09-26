# Earthquake Situation Page

Purpose: turns a public USGS GeoJSON feed into a request-time HTML dashboard.

Current behavior: fetches the feed, stringifies the JSON, embeds it into the page, and renders the visible cards in browser JavaScript.

Architecture note: this keeps the HTML Template node simple while still stress-testing network fetch, JSON payload size, HTML preview, and response output.
