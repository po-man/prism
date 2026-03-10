## Why
Currently, PRISM's data provenance (referencing) is fragmented and fragile. Impact metrics rely on an unstructured `source_citation` string for PDFs and an n8n-based text-fragment resolution step for web searches. The `source_document` field ambiguously mixes provided PDFs with web-hosted PDFs. Furthermore, financial extractions and demographic counts lack explicit provenance entirely. We need a unified, programmatic data structure for referencing that supports automated deep-linking (W3C text fragments and PDF `#page=N` routing) to allow human analysts to seamlessly verify any extracted figure or claim.

## What Changes
1.  **Unified Source Schema:** Introduce a canonical `source` object to replace all scattered provenance fields (`source_citation`, `source_url`, `source_document`, `evidence_quote`, `search_result_index`). This object will be embedded into `metrics`, `significant_events`, `beneficiaries`, and `financials`.
    * It will strictly categorize `source_type` into `["annual_report", "financial_report", "web_search"]`.
    * It will capture `page_number` (1-based absolute index) for PDFs and `search_result_index` for web results.
    * It will include the verbatim `quote` to facilitate text-fragment generation.
    * It will include a `resolved_url` field, initially `null`.
2.  **Shift Resolution Logic to Utils API:** Remove the "Resolved Text-fragment URLs" Code node from n8n. Instead, update the payload sent to the `utils_api` (`/audit` and `/validate` endpoints) to include the original report URLs and the `impact_search` array. The `utils_api` will dynamically construct and inject the `resolved_url` for every `source` object, appending `#page=N` for reports and `#:~:text=...` for web quotes.
3.  **Prompt Engineering:** Update Gemini system prompts to output the new `source` object, ensuring it extracts absolute PDF page indices rather than reading printed footers.
4.  **Frontend Updates:** Update the Hugo partials to read from the unified `source.resolved_url` and render interactive citation badges (e.g., "📄 p. 12" or "🌐 Web"), exposing the raw `quote` for visual scanning.

## Impact
- **Affected specs:** `data-schemas`, `architecture`, `audit-workflows`, `ui`
- **Affected code:** - `schemas/v1/impact.schema.json`
  - `schemas/v1/financials.schema.json`
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`
  - `n8n/prompt-templates/*`
  - `utils_api/app/routers/audit.py`
  - `utils_api/app/schemas/*`
  - `web/layouts/partials/*`