## 1. Schema Modifications (`schemas/v1/`)
- [ ] 1.1 Edit `impact.schema.json`: Add `intervention_category` to the `metrics` array items. Reference the existing enum used in `significant_events`.
- [ ] 1.2 Edit `financials.schema.json`: Add `granular_program_services` array to the `expenditure` object. Each item must contain `intervention_category` and `cost` (using `$ref: "#/definitions/financial_figure"`).
- [ ] 1.3 Ensure `utils_api/app/services/schema_loader.py` and dynamic Pydantic models cleanly inherit these changes.

## 2. Prompt Engineering (`n8n/prompt-templates/`)
- [ ] 2.1 Update `impact.system.md`: Add strict instructions to map every quantitative metric to the `intervention_category` enum. Emphasise avoiding hallucinated categorisations (use `other` if ambiguous).
- [ ] 2.2 Update `financials.system.md`: Add instructions to actively seek breakdown notes in the AFR (Annual Financial Report) and extract line-item costs into the new `granular_program_services` array using the exact same enum.

## 3. Audit Engine Refactoring (`utils_api/app/audits/`)
- [ ] 3.1 Edit `impact.py`: Completely rewrite the `calculate_cost_per_outcome` function.
- [ ] 3.2 Implement logic to check for explicit unit costs (High Confidence).
- [ ] 3.3 Implement logic to iterate through `granular_program_services` and match against `metrics` grouped by `intervention_category` (Medium/High Confidence).
- [ ] 3.4 Implement fallback logic: If granular financials are missing, calculate the percentage of total beneficiaries per `intervention_category`. If one category is >90%, allocate total `program_services` spend to it (Medium Confidence).
- [ ] 3.5 Implement abort logic: If no category is >90% and granular financials are missing, return a `LOW` confidence `cost_per_outcome` metric explaining the multi-intervention blending issue.
- [ ] 3.6 Update `tests/test_audit_impact.py` to cover these new discrete calculation pathways, testing the High/Medium/Low confidence logic tree against the new sparse matrix paradigm.

## 4. Frontend Presentation (`web/layouts/`)
- [ ] 4.1 Update `partials/myth-buster.html`: Refactor the "Value for Money" block to iterate over metrics matching `^cost_per_outcome:.*`. Render multiple cost cards if a charity successfully returns multiple granular unit costs. Implement the fallback UI for the generic `LOW` confidence blended cost.
- [ ] 4.2 Update `index.html`: Rename the "Cost per Outcome (USD)" column to "Key Interventions & Unit Costs".
- [ ] 4.3 Update `index.html`: Refactor the table cell to render a list of intervention badges (e.g., 💉, 🏠). Append the calculated cost text specifically to the matching badge.
- [ ] 4.4 Update `index.html`: Refactor the vanilla JavaScript sorting logic (`#audits-table`) to handle the new compound data structure. (Consider sorting based on the lowest available unit cost, or categorising by Tier 1/Tier 2 intervention presence).
- [ ] 4.5 Update `partials/index-how-to-read.html`: Revise the explanation text to educate users on why blended "Cost per Outcome" metrics are harmful and how to interpret the new intervention-specific sparse matrix.