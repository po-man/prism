## 1. Data Vault (PocketBase) Migrations
- [x] 1.1 Create migration script to add `gemini_cache_name` (text) and `gemini_cached` (date) fields to the `organisations` collection.

## 2. Prompt & Schema Engineering
- [x] 2.1 Consolidate `financials.system.md`, `impact.system.md` into a single `master_auditor.system.md`.
- [x] 2.2 Split the impact extraction schemas into smaller logical units (e.g., `impact_demographics.schema.json`, `impact_interventions.schema.json`, `impact_metrics.schema.json`, `impact_transparency.extract.json`).
- [ ] 2.3 Create corresponding targeted user prompt templates for each split schema.
- [x] 2.4 Update `generate_extraction_schemas.py` to handle the generation of these split schemas from the master `impact.schema.json`.

## 3. Orchestration (n8n) Refactoring
- [x] 3.1 Create a new sub-workflow: `Ensure Context Cache is on Gemini`. It should accept document URIs and the master system prompt, call the Gemini Cache API, and update the organisation's record with the cache metadata.
- [x] 3.2 Refactor the main `Charity Analysis` workflow to call the caching sub-workflow immediately after fetching the charity record and verifying document URLs.
- [x] 3.3 Replace the sequential Gemini generation nodes with parallel execution branches for Financials, and the split Impact queries, ensuring all point to the `cachedContent` URI.
- [ ] 3.4 Implement a robust Merge step to recursively combine the split JSON outputs into the standard canonical structure before submitting to `utils_api/normalize`.

## 4. Verification & Testing
- [ ] 4.1 Run an end-to-end audit on a highly complex organisation (e.g., multi-domain with large annual reports) to ensure the parallel extraction successfully merges and passes the strict `/validate` endpoint.
- [ ] 4.2 Verify cost/token reduction by comparing the new n8n execution logs against previous executions.