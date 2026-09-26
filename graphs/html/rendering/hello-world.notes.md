# Hello, World

Purpose: provide the smallest polished graph a new user can import, understand,
edit and run without credentials, network access or generative AI.

Flow:

1. **Greeting** supplies the plain text `Hello`.
2. **Complete the message** demonstrates a reusable text transformation by adding
   punctuation and `world`.
3. **Build the page** safely interpolates that message into a static HTML document.
4. **Serve the page** exposes the same document as an HTML response.

The recommended HTML panel binds directly to **Build the page**, so running the
graph immediately displays the result. Edit **Greeting** and run again to see data
flow through every downstream node.

This graph deliberately has no JavaScript, external assets, secrets or network
requests. It is intended to become the first example in `subfork-examples`.
