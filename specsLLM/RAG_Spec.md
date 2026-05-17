# AudioGen Assistant – RAG Spec

## Purpose
Retrieval-Augmented Generation (RAG) provides the model with curated knowledge about music theory, style definitions, instrumentation notes, and usage guidelines. This ensures the generated audio descriptions and parameter suggestions are accurate and grounded in authoritative sources.

## Approved Sources
- Internal audio style guide (markdown documents)
- Music theory reference (JSON)
- Instrument tone descriptions (YAML)
- Previous user session logs (anonymized, for style preference learning – optional)

## Ingestion Pipeline
1. **Collection**: Pull from approved source repositories daily.
2. **Cleaning**: Remove duplicates, formatting noise, and source documents not on the approved list.
3. **Chunking**:
   - **Chunk size**: 512 tokens (empirically validated with golden prompts).
   - **Overlap**: 15% (approximately 77 tokens) to preserve boundary context.
4. **Embedding**: Convert each chunk to a 768‑dim vector using `text-embedding-ada-002` (or equivalent).
5. **Storage**: Vector database + inverted index for hybrid retrieval.

## Metadata Schema
Every chunk carries the following fields:

| Field          | Type   | Description                          |
|----------------|--------|--------------------------------------|
| `source`       | string | Document ID                          |
| `date`         | string | ISO 8601 date                        |
| `owner`        | string | Team name                            |
| `access_rights`| array  | Roles permitted (e.g., `["admin"]`)  |
| `document_type`| string | One of: `style_guide`, `theory`, `instrument`, `log` |
| `chunk_id`     | int    | Sequential identifier                |

## Retrieval Strategy
- **Primary**: Hybrid retrieval (vector + keyword BM25) with a 1:1 ratio.
- **Reranking**: Cross‑encoder reranker (`cross-encoder/ms-marco-MiniLM-L-6-v2`) to re‑score top‑20 results.
- **Final top‑k**: 5 chunks returned.
- **Pre‑filters**: Enforce `access_rights` matching the user role; filter by `document_type` based on query intent.

## Grounding Rules
1. **Cite the source**: Every claim derived from a chunk must include the source ID in the `sources` array of the output schema.
2. **No evidence, no answer**: If no relevant chunk is retrieved for a factual question, the assistant must say “I don’t have enough information to answer that” – never hallucinate.
3. **Separate evidence from inference**: Paraphrased content from a chunk must be marked with `(based on [source])`; the model’s own reasoning should be clearly distinguishable.
4. **Log grounding failures**: Every response where `confidence > 0.7` but `sources` array is empty must be flagged in monitoring.

## Anti‑Injection Measures
- Retrieved chunks are treated as **untrusted input**.
- System instructions are structurally separated from chunk text using special delimiters in the prompt template.
- Chunks containing suspicious instruction‑like patterns (e.g., “ignore previous instructions”) are sanitized before injection.
- All tool calls are validated independently of any chunk content.