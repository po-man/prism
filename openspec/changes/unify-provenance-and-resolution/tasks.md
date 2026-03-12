# openspec/changes/unify-provenance-and-resolution/tasks.md

## 1. JSON Schema Updates (`schemas/v1/`)
- [x] 1.1 In `impact.schema.json`:
  - Define a new `source` object definition under a `"definitions"` block (or inline if preferred) containing: `source_type` (enum: `annual_report`, `financial_report`, `web_search`), `page_number` (integer, nullable), `search_result_index` (integer, nullable), `quote` (string, nullable), and `resolved_url` (string/uri, nullable).
  - Update `beneficiaries.items.properties` to include an optional `source` object.
  - Update `metrics.items.properties` to include a required `source` object. Remove `source_citation`, `source_url`, `source_document`, `evidence_quote`, and `search_result_index`.
  - Update `significant_events.items.properties` to include a required `source` object. Remove `source_url`, `source_document`, `source_quote`, and `search_result_index`.
- [x] 1.2 In `financials.schema.json`:
  - Add a `sources` array to the root properties, where `items` match the unified `source` object definition from 1.1. 

## 2. Utils API Updates (`utils_api/`)
- [x] 2.1 Refactor `app/schemas/url_resolver.py` to `app/schemas/provenance.py`. 
  - Define `ProvenanceContext` model (fields: `annual_report_url` (str), `financial_report_url` (str), `web_search_results` (list of dicts)).
  - Define `ProvenanceRequest` model (fields: `data` (dict), `context` (ProvenanceContext)).
- [x] 2.2 Rename `app/routers/url_resolver.py` to `app/routers/provenance.py` and update `main.py` router inclusion.
- [x] 2.3 Implement the `POST /resolve-provenance` endpoint:
  - Traverse the incoming `data` dictionary recursively to find any dictionaries matching the `source` object signature (having `source_type` and `resolved_url` keys).
  - If `source_type == 'annual_report'` and `page_number` exists: Set `resolved_url = f"{context.annual_report_url}#page={page_number}"`.
  - If `source_type == 'financial_report'` and `page_number` exists: Set `resolved_url = f"{context.financial_report_url}#page={page_number}"`.
  - If `source_type == 'web_search'` and `search_result_index` exists: Fetch the item from `context.web_search_results`. Set `resolved_url = {base_url}#:~:text={encoded_quote}` using the existing W3C fragment logic. If it is a 301/302 redirect, resolve it using `httpx` (reusing the existing redirect logic).
- [x] 2.4 Update `tests/shared.py` to match the new schema structure (replacing `evidence_quote`, `source_citation`, etc., with the new `source` objects in `VALID_BASE_RECORD` and `VALID_IMPACT`).
- [x] 2.5 Update `tests/test_validation.py` and `tests/test_audit_impact.py` to reflect the schema changes and assert against `metric["source"]["quote"]` instead of `metric["evidence_quote"]`.
- [ ] 2.6 Add unit tests in `tests/test_provenance.py` for `/resolve-provenance` to verify PDF fragment appending and W3C text fragment generation.

## 3. Prompt Engineering (`n8n/prompt-templates/`)
- [x] 3.1 In `impact.system.md`:
  - Add explicit instructions: "All extracted data points MUST include a `source` object to guarantee provenance."
  - Add a strict instruction for PDFs: "For PDF documents, `page_number` MUST be the 1-based absolute index of the PDF file. Do NOT read the printed page number in the document's footer or header (e.g., ignore Roman numerals or offset numbers)."
  - Replace references to `evidence_quote` and `source_quote` with the new `source.quote` instruction.
- [x] 3.2 In `financials.system.md`:
  - Add instructions to populate the `sources` array with the primary pages used to extract the financial statements, adhering to the absolute 1-based PDF index rule.

## 4. Orchestrator Updates (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [x] 4.1 Delete the existing "Resolve URLs (Impact Search)" HTTP Request node and the "Resolved Text-fragment URLs (Impact Metrics)" Code node.
- [x] 4.2 Create a new HTTP Request node called "Resolve Provenance (Impact)" placed after the "Extract Impact Metrics" and "Parsed Content (Impact Metrics)" nodes.
  - Method: POST
  - URL: `={{ $('Vars - Utils API & Schemas').first().json.utils_api_host }}/resolve-provenance`
  - Body: Construct the JSON payload with `data` = `{{ $json.parsedContentObject }}` and `context` = `{ annual_report_url: ..., financial_report_url: ..., web_search_results: ... }`. Read URLs from the `Storage API - Get Charity` node.
- [x] 4.3 Create a new HTTP Request node called "Resolve Provenance (Financials)" placed after the "Parsed Content (Financials)" node.
  - Configure similarly to 4.2, passing the parsed financials and the report URLs as context.
- [x] 4.4 Reroute the outputs of these new nodes into their respective "Schema Validation" nodes.
- [x] 4.5 Update the "Storage API - Update Charity - Impact" and "Storage API - Update Charity - Financials" nodes to save the resolved data rather than the raw parsed LLM output.

## 5. Frontend / UI Updates (`web/layouts/`)
- [ ] 5.1 In `partials/impact-item.html`:
  - Update variable references from `.url`, `.quote`, `.source_document` to expect the unified `source` object properties (`.source.resolved_url`, `.source.quote`, `.source.source_type`).
  - Render a small interactive badge linking to `source.resolved_url` with `target="_blank"`. Use a generic document icon for reports and a globe icon for `web_search`.
  - Render a `<details>` element (or a clean tooltip) adjacent to the badge that displays the `source.quote` so the user knows what text to look for on the linked page.
- [ ] 5.2 In `partials/demographic-item.html`:
  - Add logic to check for the presence of the `source` object on the beneficiary item. If present, render the same citation badge/quote dropdown.
- [ ] 5.3 In `partials/impact-pathway.html` (Inputs section):
  - Check if `financials.data.sources` exists and has length > 0.
  - If present, render citation badges next to the "Total Annual Expenditure" value, linking to the absolute PDF pages where the financials were sourced.
- [ ] 5.4 Ensure visual alignment with `web/assets/css/custom.css` so the badges and `<details>` elements do not break the existing flexbox layouts.