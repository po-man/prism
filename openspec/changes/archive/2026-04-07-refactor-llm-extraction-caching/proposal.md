## Why
Currently, PRISM processes multi-page PDF reports by passing the entire document context to the Gemini API separately for Financials, Impact, and Metadata extractions. This redundant processing leads to excessive token consumption, high API latency, and degraded LLM accuracy when extracting complex, nested schemas (especially for Impact data).

## What Changes
- **Implement Gemini Context Caching:** Cache the combined system prompt and source documents (Annual and Financial reports) for each organisation's analysis batch.
- **Unify System Prompts:** Create a single `master_auditor.system.md` to be embedded in the context cache, defining the global PRISM auditor persona and EA provenance rules.
- **Split User Prompts and Schemas:** Deconstruct the monolithic `impact.schema.json` into modular sub-schemas (e.g., beneficiaries, events, metrics, transparency).
- **Parallelise n8n Workflows:** Update the primary n8n workflow to execute the split user prompts concurrently against the cached context, merging the results prior to validation.

## Impact
- **Affected specs:** `architecture` (Caching and prompt management).
- **Affected code:** n8n workflows (`SUjUpjve9Vj6aJSbbuIWL.json`, `7WmUvPfyMRFCI864.json`), PocketBase schema (`organisations`), Prompt Templates, Schema Extraction Script (`generate_extraction_schemas.py`).