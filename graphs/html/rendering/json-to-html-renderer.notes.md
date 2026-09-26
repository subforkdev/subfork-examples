# JSON To HTML Renderer

Purpose: baseline proof that a graph can render structured JSON into HTML and return it through an HTML response node.

Current behavior: static JSON feeds the HTML Template node, which emits both raw HTML and an HTTP-style HTML response.

Architecture note: this is the smallest useful "page graph" shape and does not require site, domain, or route concepts.
