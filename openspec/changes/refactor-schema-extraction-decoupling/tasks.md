# openspec/changes/refactor-schema-extraction-decoupling/tasks.md

## 1. Schema Metadata Enrichment (`schemas/v1/`)
- [ ] 1.1 Edit `impact.schema.json`: Identify properties with excessively long names (e.g., `intervention_type_other_description`, `unintended_consequences_reported`, `euthanasia_statistics_reported`) and inject the `"x-extract-key"` property with a terse equivalent (e.g., `other_desc`, `unintended_rep`, `euthanasia_rep`).
- [ ] 1.2 Edit `financials.schema.json`: Apply the `"x-extract-key"` property to lengthy keys such as `provident_fund_reserve` and `monthly_operating_expenses`.

## 2. Build Script Implementation (`scripts/`)
- [ ] 2.1 Create `scripts/generate_extraction_schemas.py`.
- [ ] 2.2 Implement the Abstract Syntax Tree (AST) traversal logic to parse canonical schemas from `schemas/v1/`.
- [ ] 2.3 Implement the **Field Pruning** function: Target and delete `definitions.source.resolved_url` (which contains the problematic `"format": "uri"`) from the schema tree.
- [ ] 2.4 Implement the **Enum Transformation** function: Locate all `"enum"` arrays, extract the values, delete the `"enum"` key, set `"type": "string"`, and append `[ALLOWED VALUES: 'val1', 'val2', ...]` to the `"description"`.
- [ ] 2.5 Implement the **Semantic Shortening** function: Swap keys containing `"x-extract-key"`, prepend the humanised original key name to the `"description"`, and populate a global dictionary with the mapping.
- [ ] 2.6 Configure the script to output the lightweight schemas as `*.extract.schema.json` within the `schemas/v1/` directory and export the mapping dictionary as `schemas/v1/key_mapping.json`.

## 3. Microservice Reversal Logic (`utils_api/`)
- [ ] 3.1 Create `utils_api/app/services/schema_mapper.py` to house the recursive key-reversal algorithm.
- [ ] 3.2 Implement a function `reverse_extracted_keys(payload: dict, mapping_file: str = "key_mapping.json") -> dict` that recursively traverses the raw LLM JSON payload and swaps any abbreviated keys back to their canonical forms.
- [ ] 3.3 Create a new endpoint in `utils_api/app/routers/validation.py` (e.g., `POST /normalize-extraction`) that accepts the raw LLM payload, applies `reverse_extracted_keys`, and returns the canonicalised JSON ready for standard validation.
- [ ] 3.4 Add unit tests in `utils_api/tests/test_validation.py` to verify that the reversal logic correctly restores deeply nested keys and leaves unmapped keys untouched.

## 4. Orchestrator Integration (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 4.1 Update the `Vars - Utils API & Schemas` Set node to define new string variables for the extraction schemas (e.g., `financials_extract_schema: v1/financials.extract.schema.json`).
- [ ] 4.2 Update the `Read JSON schema (Financials)`, `Read JSON schema (Impact)`, and `Read JSON schema (Impact Search)` nodes to target these new `*.extract.schema.json` variables for prompt injection.
- [ ] 4.3 Insert an HTTP Request node immediately after each Gemini extraction node (e.g., after `Extract Financials` and `Extract Impact Metrics`) to call the new `utils_api/normalize-extraction` endpoint.
- [ ] 4.4 Ensure the subsequent `Schema Validation` HTTP Request nodes receive the normalised (canonical) JSON payload from the normalisation node, preserving the existing validation flow.