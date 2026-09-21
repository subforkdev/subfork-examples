# OpenAI Read Aloud

<a href="../openai-read-aloud.subfork.json" download="openai-read-aloud.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Read a short text aloud with an editable voice and delivery prompt. The graph
passes the supplied wording directly to speech synthesis; it does not summarize
or rewrite it. The voice is AI-generated.

## Try it

1. Import the graph and add the graph-scoped secret `OPENAI_API_KEY` in
   Graph Settings > Execution Profile.
2. Edit **Text to read**, **Voice direction**, and optionally **Voice**.
   The default voice is `marin`; `cedar` is another option.
3. Run. Bind Audio Preview to **Generate speech → media**. The `transcript`
   graph output contains the supplied script, and `response` serves the MP3.

The built-in sample is original fictional text. No upload is required, and this
example works on a localhost dev instance with outbound access to OpenAI.

## Graph and limits

`Text + voice + delivery prompt → validate → speech body → HTTP request → audio`

- One paid `POST https://api.openai.com/v1/audio/speech` call using
  `gpt-4o-mini-tts`. Script and voice instructions are sent to OpenAI.
- Script: 1–3500 characters, including at least one non-whitespace character.
  Voice instructions: 1–1000 characters. Voice must be one of the built-in options
  listed in the validation node. These are example limits, not provider maxima.
- Timeout: 120 seconds. Response cap: 10,000,000 bytes. One audio track; no loops,
  automatic retries, chapter splitting, concatenation, or background jobs.
- A validation failure stops before the paid call. Each regex check feeds its
  match collection into JSON Path `0`; an empty collection deliberately fails.
  The failing node's title identifies the limit to fix.
- Inspect **Generate speech → status/json** for provider errors such as missing
  credentials, model access, or rate limits. A failed request produces no audio.
- Audio uses the runtime's existing media/artifact behavior. No generated media
  or credentials are included in this export. Running again can incur another
  charge. There is no publication, messaging, or deletion step.

To read text from a PDF without adaptation, paste a short extracted passage into
**Text to read**. For PDF upload and prompted adaptation, use
[OpenAI PDF Narration](openai-pdf-narration.notes.md).

## Validation

The graph is checked against the sibling runtime with mocked provider responses.
Live voice quality and paid API execution still need testing in your instance.

[OpenAI speech guide](https://developers.openai.com/api/docs/guides/text-to-speech)

To repeat offline checks from the examples repository:

```sh
python3 scripts/check_narration_examples.py --runtime-root ../subfork-new/backend/runtime
```

The runtime path is a CLI argument and can point to another checkout. No provider
credentials or network access are used by these checks.
