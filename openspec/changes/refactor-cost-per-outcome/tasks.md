## 1. Schema Updates (`schemas/v1/`)
- [x] 1.1 Update `impact.schema.json`: Replace the `explicit_unit_cost` object with an `explicit_unit_costs` array of objects. Add the `intervention_type` field referencing `InterventionTypeEnum` to each object.
- [x] 1.2 Update `financials.schema.json`: Add a `program_breakdowns` array to the `expenditure` object, containing `programme_name` and an `amount` referencing `financial_figure`.
- [x] 1.3 Run `python scripts/generate_extraction_schemas.py` to regenerate the `.extract.schema.json` variants for the LLM.

## 2. Prompt Template Updates (`n8n/prompt-templates/`)
- [ ] 2.1 Update `impact.system.md`: Instruct the LLM to actively extract an array of explicitly stated costs for specific interventions (e.g., "Sponsor a farm rescue for £50").
- [ ] 2.2 Update `financials.system.md`: Instruct the LLM to extract granular line-item programmatic spending from the statement of comprehensive income or notes to the accounts into the `program_breakdowns` array.

## 3. Audit Engine Updates (`utils_api/app/audits/`)
- [ ] 3.1 Modify `app/schemas/impact.py` and `app/schemas/financials.py` Pydantic models to reflect the new schema arrays (`explicit_unit_costs` and `program_breakdowns`).
- [ ] 3.2 Rewrite `calculate_cost_per_outcome` in `app/audits/impact.py` to process the `explicit_unit_costs` array first, returning a HIGH confidence array of costs if found.
- [ ] 3.3 Implement the programmatic matching logic: Attempt to align `program_breakdowns` with specific `significant_events` using basic string matching or allocation thresholds.
- [ ] 3.4 Implement the Pure-Play cohort logic: Check if >80% of `program_services` spend goes to a single programme. If so, execute the division and return as MEDIUM confidence.
- [ ] 3.5 Ensure the fallback gracefully returns a LOW confidence `null` for unattributable multi-domain portfolios.
- [ ] 3.6 Update `tests/test_audit_impact.py` to provide coverage for the array extraction, pure-play detection, and multi-domain abortion scenarios.

## 4. Frontend Rendering Updates (`web/layouts/partials/`)
- [ ] 4.1 Update `myth-buster.html` to handle the new calculation output format from `utils_api`.
- [ ] 4.2 Add Go/Hugo template logic to iterate over arrays of costs, rendering each intervention type and its associated cost cleanly.
- [ ] 4.3 Add conditional UI logic to display a "Pure-Play Benchmark" tag if the cost was derived using the cohort methodology.