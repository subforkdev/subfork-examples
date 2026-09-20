# Markdown-ish Content Page

Purpose: tests authoring longer text content and wrapping it in a readable HTML page.

Current behavior: a multiline text value is escaped by the template renderer and displayed in a `<pre>` block.

Architecture note: this is deliberately not a Markdown renderer yet; add a Markdown node later if the pattern earns it.
