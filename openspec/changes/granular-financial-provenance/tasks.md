## 1. JSON Schema Updates (`schemas/v1/`)
- [x] 1.1 Edit `financials.schema.json` to remove the root-level `sources` array.
- [x] 1.2 Add a new definition under `"definitions"` called `financial_figure`:
  ```json
  "financial_figure": {
    "type": "object",
    "properties": {
      "value": { "type": ["number", "null"] },
      "source": { "$ref": "#/definitions/source", "type": ["object", "null"] }
    },
    "required": ["value"]
  }
  ```
- [x] 1.3 Refactor all properties inside `income`, `expenditure`, `lsg_specifics`, `reserves`, and `ratio_inputs` to `$ref` the `#/definitions/financial_figure` schema instead of directly taking a `["number", "null"]`.

## 2. Utils API Updates (`utils_api/`)
- [ ] 2.1 In `app/audits/financial.py`:
  - Update `check_reserve_cap` to reference `.value`: e.g., `reserve = record.financials.reserves.total_reserves.value` and `expenditure = record.financials.expenditure.total.value`. Ensure `None` checks handle the nested structure gracefully.
  - Update `check_liquidity` similarly for `net_current_assets.value`, `monthly_operating_expenses.value`, `current_assets.value`, and `current_liabilities.value`.
- [ ] 2.2 In `app/audits/impact.py`:
  - Update `check_funding_neglectedness` to use `record.financials.income.government_grants.value` and `record.financials.income.total.value`.
  - Update `calculate_cost_per_outcome` to use `record.financials.expenditure.program_services.value`.
- [ ] 2.3 In `tests/shared.py`:
  - Refactor `VALID_FINANCIALS` and `VALID_BASE_RECORD["financials"]` to use the nested `{"value": X, "source": {...}}` format for all financial figures. Remove the top-level `sources` array.
- [ ] 2.4 Run `pytest` within the `utils_api` container to ensure all assertions pass with the newly defined schema structure.

## 3. Prompt Engineering (`n8n/prompt-templates/`)
- [x] 3.1 In `financials.system.md`:
  - Delete the instruction regarding populating the top-level `sources` array.
  - Add an explicit instruction: "For **every** extracted financial figure, you MUST populate its nested `source` object. The `page_number` MUST be the 1-based absolute index of the PDF file... For each line-item source, extract an exact, verbatim quote...".

## 4. Orchestrator Updates (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 4.1 Locate the "Resolve Provenance (Financials)" HTTP Request node. Update the JSON body so that the `data` parameter passes the entire financials object (`{{ JSON.stringify($json.parsedContentObject) }}`) instead of the defunct `.sources` array.
- [ ] 4.2 Locate the "Merge Provenance (Financials)" Code node. Update the JavaScript logic. Since the API will now return the fully resolved financials tree, simply assign `item.json.parsedContentObject = item.json.data;` and delete `item.json.data;`.

## 5. Frontend / UI Updates (`web/layouts/`)
- [ ] 5.1 In `partials/impact-pathway.html`:
  - Refactor references: change `$financials.expenditure.total` to `$financials.expenditure.total.value`.
  - Remove the loop over the defunct `$financials.sources`.
  - Render the badge for the total expenditure: `{{ with .financials.data.expenditure.total.source }}{{ partial "provenance-badge.html" . }}{{ end }}`.
- [ ] 5.2 In `partials/myth-buster.html`:
  - Update variable assignments to access `.value`: e.g., `{{ $total_exp := .financials.data.expenditure.total.value }}`. Apply this to `$prog_exp`, `$admin_exp`, and `$fundraising_exp`.
- [ ] 5.3 Test the Hugo build to guarantee it generates templates without errors and visually verifies the new line-item provenance badges are correctly rendered.