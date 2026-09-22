# OpenAI PDF Narration

<a href="../openai-pdf-narration.subfork.json" download="openai-pdf-narration.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Upload a short PDF and ask for a spoken adaptation. The graph produces a narration
transcript and one MP3 with an AI-generated voice. It is a short-document example,
not a complete audiobook production system or a verbatim PDF reader.

## Runtime prerequisite

This example requires the new **File Asset** node (`n_file_asset`, version
`1.0.0`), the `/graphs/{graph_id}/assets/files` upload route, and the inspector's
file-upload control. Update the API, frontend, node catalog, and execution workers
with that support before importing. Earlier Subfork versions will not recognize
the node.

OpenAI fetches a temporary signed artifact URL. Your dev instance or configured
object storage must be reachable by OpenAI; a localhost-only URL will not work.
For a localhost speech test, start with [OpenAI Read Aloud](openai-read-aloud.notes.md).

## Try it

1. Import and save the graph. Add the graph-scoped secret `OPENAI_API_KEY` in
   Graph Settings > Execution Profile. No OpenAI file ID or other secret is needed.
2. Select **Upload PDF** and upload a small PDF, ideally 1–3 pages for the first
   run. Start with ordinary selectable text. The shipped artifact ID is empty;
   each imported graph needs its own upload.
3. Edit **Narration prompt**, for example: “Explain this to a curious beginner
   in about two minutes. Preserve the main ideas and concrete examples.”
4. Edit **Voice direction** to control delivery separately from the content.
   **Voice** defaults to `marin`; try `cedar` to compare.
5. Run. Bind Audio Preview to **Generate speech → media** and a text/JSON panel
   to **Narration transcript → value**. The `transcript`, `audio`, `response`,
   `speech_status`, and `narration_result` graph outputs are also available.

## Graph and limits

`PDF artifact URL + prompt → Responses API → validate completed narration → speech → MP3`

- File Asset accepts PDF or UTF-8 text, but this graph checks `media_type` and
  requires a PDF. Upload size uses the instance's `graph_media_max_bytes` setting
  (5 MB by default). PDF header/end-marker checks do not guarantee a valid PDF;
  the provider may reject malformed or encrypted documents.
- One paid `POST https://api.openai.com/v1/responses` request using
  `gpt-4.1-mini`, with `store: false`, a 120-second timeout, a 250,000-byte response
  cap, and `max_output_tokens: 900`. OpenAI receives the prompt and signed URL and
  fetches the entire PDF, including page images. Larger PDFs can increase input
  costs. This graph has no page-count enforcement or local OCR/extraction step.
- Narration prompt: 1–2000 characters. The model is asked for fewer than 3000
  characters. A hard graph check rejects empty/whitespace-only scripts and scripts
  over 3500 characters before speech generation; nothing is silently truncated.
- The response must have status `completed`. Output items are filtered by type
  so a non-message item does not shift the transcript selection. Refusals without
  output text, missing output, and incomplete responses stop before speech.
- One paid `POST https://api.openai.com/v1/audio/speech` request using
  `gpt-4o-mini-tts`, with a 120-second timeout and a 10,000,000-byte response cap.
  The narration and delivery instructions are sent to OpenAI. Voice instructions
  are limited to 1000 characters and the voice is checked against built-in options.
- At most two provider POSTs per successful run; no automatic retries, iteration,
  chapter navigation, audio concatenation, or long-running job polling.

The transcript is generated and may omit or misinterpret source material. It is
shown for inspection but is not an approval gate: a valid completed script goes
straight to speech. Generation time, duration, pronunciation, and narration quality
are not guaranteed. If generation hits the output cap, ask for a shorter result.

## Storage, visibility, and troubleshooting

The PDF is stored as a graph asset under existing storage quotas. Upload alone
makes no OpenAI call. Execution creates a temporary provider URL and sends the
PDF to OpenAI. `store: false` is not a promise of zero provider retention.
Publishing the graph follows existing graph-asset visibility rules and can expose
its referenced document. Do not publish private documents or commit artifact IDs,
provider URLs, keys, or generated audio in portable exports.

Each validation node feeds regex matches into JSON Path `0`; an empty match list
intentionally fails. Use the failing node title to locate invalid input. Inspect
**Generate narration → status/json** or **Generate speech → status/json** for
provider errors. Missing uploads fail at File Asset before any provider call.
A speech failure can still follow a billable narration request. Rerunning can
charge for both stages again. There are no deletion or messaging steps.

## Validation

The graph is checked against the sibling runtime with mocked provider responses,
including incomplete generation, refusal, invalid input, and oversized narration.
Live PDF fetching and paid voice generation still need testing in your instance.

[OpenAI file inputs](https://developers.openai.com/api/docs/guides/file-inputs) ·
[OpenAI speech guide](https://developers.openai.com/api/docs/guides/text-to-speech)

To repeat offline checks from the examples repository:

```sh
python3 scripts/check_narration_examples.py --runtime-root ../subfork-new/backend/runtime
```

The runtime path is a CLI argument and can point to another checkout. No provider
credentials or network access are used by these checks.
