## 1. Data Vault & Schema Updates
- [x] 1.1 Create PocketBase migrations for `ref_moral_weights`, `ref_evidence_discounts`, and `ref_intervention_baselines` collections.
- [x] 1.2 Seed the new reference collections with consensus EA data (e.g., GiveWell/Rethink Priorities estimates).
- [x] 1.3 Update `schemas/v1/impact.schema.json` to ensure `species`, `evidence_claim`, and `intervention_typology` are strictly defined for extraction.
- [x] 1.4 Update `schemas/v1/analytics.schema.json` to accommodate the IES payload inside `calculated_metrics`.
- [x] 1.5 Run `scripts/generate_extraction_schemas.py` to compile the updated LLM extraction schemas.

## 2. Logic Layer (`utils_api`)
- [x] 2.1 Implement a PocketBase client service in Python to fetch reference data (W_species, D_evidence) during the audit phase.
- [x] 2.2 Create `calculate_ies` function in `app/audits/impact.py`.
- [x] 2.3 Implement the deterministic BOTEC logic within `calculate_ies` to generate the Expected Value using solely extracted claims and PocketBase baseline multipliers, avoiding external API dependencies.
- [x] 2.4 Register `calculate_ies` in `app/audits/registry.py` under `METRIC_CALCULATORS`.
- [ ] 2.5 Write unit tests in `tests/test_audit_impact.py` to verify the deterministic math of the IES formula.

## 3. Frontend (`web`)
- [x] 3.1 Create a new Hugo partial `web/layouts/partials/ies-scorecard.html`.
- [x] 3.2 Implement the UI logic to parse the IES metric from `analytics.calculated_metrics` and display the mathematical breakdown ($Outcomes_i \times W_{species} \times W_{leverage} \times D_{evidence}$).
- [x] 3.3 Add styling in Tailwind CSS to visually differentiate empirical extracted data from hardcoded EA constants.
- [x] 3.4 Inject `{{ partial "ies-scorecard.html" $org }}` into `web/layouts/_default/single.html`.
