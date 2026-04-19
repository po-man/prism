## 1. Schema & Database Updates
- [x] 1.1 Delete `schemas/v1/search.schema.json` and `schemas/v1/search.schema.extract.schema.json`.
- [x] 1.2 Open all remaining schemas (`impact.schema.json`, `financials.schema.json`, etc.) and their extraction counterparts. 
    - In the `source` definition, remove `"web_search"` from the `source_type` enum.
    - Delete the `search_result_index` property.
- [x] 1.3 Create a new PocketBase migration script in `pocketbase/migrations/` to drop the `impact_search` JSON column from the `organisations` collection.

## 2. Prompt Engineering (`n8n/prompt-templates`)
- [x] 2.1 Delete `impact-search.system.md` and `impact-search.user.md`.
- [x] 2.2 Open `impact.system.md`. Under "Context Hierarchy and Provenance", remove references to `<web_context>` snippets and the instruction to "Prioritize PDF data over web snippets". Remove instructions to populate `search_result_index`.

## 3. n8n Orchestrator Updates (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 3.1 Open the main Charity Analysis workflow.
- [ ] 3.2 Delete the entire Impact Search branch: `Search for Impact Snippets`, `Call 'Prompt Injection' - Impact Search`, `Schema Validation (Impact Search)`, `Parsed Content (Impact Search)`, `Resolve URLs (Impact Search)`.
- [ ] 3.3 Update the `Storage API - Update Charity - Impact` node. Remove `impact_search` from the payload body.
- [ ] 3.4 Update all `Merge` nodes that previously waited on the Impact Search branch (e.g., `Merge (Impact - Beneficiaries)`) to only combine inputs from the PDF extractions.
- [ ] 3.5 Update all `Resolve Provenance` HTTP Request nodes. Remove `web_search_results` from the JSON body payload.
- [ ] 3.6 Update all `Extract Impact - [Domain]` HTTP Request nodes. Remove the dynamic injection of the `impact_search` data into the Gemini prompt payload.

## 4. Python Audit Engine (`utils_api`)
- [x] 4.1 Delete `utils_api/app/routers/url_resolver.py` and remove its router inclusion from `utils_api/app/main.py`. Delete `utils_api/app/schemas/url_resolver.py` and `search.py`.
- [x] 4.2 In `utils_api/app/schemas/provenance.py`, remove `web_search_results` and `WebSearchResult` from the `ProvenanceContext`.
- [x] 4.3 In `utils_api/app/routers/provenance.py`:
    - Remove the `_resolve_redirect` function.
    - Remove all logic pertaining to `source_type == "web_search"`, `search_result_index`, and W3C Text Fragment encoding.
    - Update the `/resolve-provenance` endpoint to remove `web_search_urls` mapping.
- [x] 4.4 Update `utils_api/tests/test_provenance.py` and `utils_api/tests/shared.py` to remove web search mocked data and corresponding assertions.

## 5. UI / Hugo Refactoring (`web`)
- [ ] 5.1 Delete `web/layouts/partials/logic/has-web-source.html`.
- [ ] 5.2 Delete `web/layouts/partials/icons/web-search.svg`.
- [ ] 5.3 In `web/layouts/_default/single.html`:
    - Remove the "Web Search" icon rendering logic and the `$has_web_source` variable block under Data Sources.
- [ ] 5.4 In `web/layouts/index.html` (Master Table):
    - Remove the `$has_web_source` variable evaluation.
    - Remove the "Web Search" icon from the "Data Sources" column.
    - Update `$s.Add "sourceCount" 1` logic to only count to a maximum of 2 (Annual and Financial).
- [ ] 5.5 In `web/layouts/partials/provenance-badge.html`:
    - Delete the `{{ else if eq .source_type "web_search" }}` block entirely.
    - Update the tooltip text to remove web specific terminology if present.
- [ ] 5.6 In `web/layouts/partials/index-how-to-read.html` (How to Read This Table):
    - Update any mention of web search in the Data Sources explanation.