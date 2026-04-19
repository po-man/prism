## Why
PRISM's core value proposition is operating as a strict, deterministic audit engine for animal advocacy charities. Currently, the platform supplements missing PDF report data with unstructured snippets scraped from the charity's website. However, web snippets introduce an unacceptably high degree of noise, marketing fluff, and temporal ambiguity (e.g., a website claiming "we saved 10,000 animals" rarely specifies if this is an annual, verifiable figure or a historical, cumulative estimate). To maintain strict Effective Altruism (EA) data fidelity and provenance, we must enforce a "no-inference, audited-documents-only" boundary, removing the web search vector entirely.

## What Changes
1. **Schema & Database:** Delete `search.schema.json`. Remove the `web_search` enum value and `search_result_index` from the unified `source` object definition across all impact and financial schemas. Create a PocketBase migration to drop the `impact_search` JSON field from the `organisations` collection.
2. **Orchestrator (n8n):** Prune the entire web search branch from the main `SUjUpjve9Vj6aJSbbuIWL` pipeline. This includes removing the Google Search API node, prompt injections for search, and the URL resolution steps. Merge nodes will be updated to only await PDF document extractions.
3. **Prompt Engineering:** Remove all instructions regarding `<web_context>` and evidence hierarchy (PDF vs. Web) from the Gemini system prompts, as the LLM will now exclusively ingest formal reports.
4. **Audit Engine (`utils_api`):** Remove the `/resolve-search-urls` endpoint from `url_resolver.py` and strip web-search specific handling from `provenance.py`.
5. **UI (Hugo):** Remove all "Web Search" globe icons, provenance badging logic, and the `has-web-source.html` partial from the frontend templates to reflect the tightened data boundary.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/*`, `pocketbase/migrations/*`, `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`, `n8n/prompt-templates/*`, `utils_api/app/routers/*`, `web/layouts/*`