# OpenAI PDF Narration

[Download graph](openai-pdf-narration.subfork.json)

Provide a public PDF URL and a prompt to generate a short narration transcript and one MP3 with an AI-generated voice. This is a short-document example, not an audiobook system or verbatim PDF reader.

## Try it

1. Import the graph and add the graph-scoped `OPENAI_API_KEY` secret.
2. Set **Public PDF URL** to an HTTPS PDF that OpenAI can fetch without Subfork credentials.
3. Edit the narration prompt, voice direction, and voice, then run. Bind Audio Preview to the generated speech and a text or JSON panel to the transcript.

The current generic HTTP request node does not accept a private Subfork artifact for provider delivery. This is deliberate: an ordinary graph URL must not become a bearer grant for private content or allow arbitrary credentialed exfiltration. Use a URL whose publication and retention you control. A future OpenAI-specific adapter may accept an `artifact` input, validate PDF type and size, issue a minimum-scope provider grant out of band, and retain provider media as an execution-output artifact.

The graph makes one paid Responses API request with `store: false`, a 120-second timeout, a 250,000-byte response cap, `max_output_tokens: 900`, and then one paid speech request with a 120-second timeout and 10,000,000-byte response cap. Prompt length is limited to 2000 characters; generated narration is validated before speech. The public PDF, prompt, transcript, and voice instructions are sent to OpenAI. Rerunning can create new charges.

The transcript may omit or misinterpret source material. Provider errors and invalid responses stop the graph before later work where possible. The generated MP3 is retained as an execution artifact; the graph does not publish or delete it. No public URL, key, artifact ID, or generated audio is shipped in the export.
