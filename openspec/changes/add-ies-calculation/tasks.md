# openspec/changes/add-ies-calculation/tasks.md

## 1. Data Vault & Schema Updates
- [x] 1.1 Create PocketBase migrations for `ref_moral_weights`, `ref_evidence_discounts`, and `ref_intervention_baselines` collections.
- [x] 1.2 Seed the new reference collections with consensus EA data (e.g., GiveWell/Rethink Priorities estimates).
- [ ] 1.3 Update `schemas/v1/impact.schema.json` to ensure `species`, `evidence_claim`, and `intervention_typology` are strictly defined for extraction.
- [ ] 1.4 Update `schemas/v1/analytics.schema.json` to accommodate the IES payload inside `calculated_metrics`.
- [ ] 1.5 Run `scripts/generate_extraction_schemas.py` to compile the updated LLM extraction schemas.

## 2. Logic Layer (`utils_api`)
- [ ] 2.1 Implement a PocketBase client service in Python to fetch reference data ($W_{species}$, $D_{evidence}$) during the audit phase.
- [ ] 2.2 Implement external API integration modules (e.g., FAOSTAT wrapper for animal populations, World Bank wrapper for PPP adjustments).
- [ ] 2.3 Create `calculate_ies` function in `app/audits/impact.py`.
- [ ] 2.4 Implement the systemic BOTEC logic within `calculate_ies` to generate $W_{leverage}$ based on intervention typology and region.
- [ ] 2.5 Register `calculate_ies` in `app/audits/registry.py` under `METRIC_CALCULATORS`.
- [ ] 2.6 Write unit tests in `tests/test_audit_impact.py` to verify the deterministic math of the IES formula.

## 3. Orchestration (`n8n`)
- [ ] 3.1 Update the Prompt Templates (`impact.user.md`, `impact.system.md`) to explicitly instruct Gemini to extract the required IES variables as `null` if absent.
- [ ] 3.2 Update the `SUjUpjve9Vj6aJSbbuIWL.json` workflow to ensure the `/audit` HTTP request correctly maps the new extracted fields.

## 4. Frontend (`web`)
- [ ] 4.1 Create a new Hugo partial `web/layouts/partials/ies-scorecard.html`.
- [ ] 4.2 Implement the UI logic to parse the IES metric from `analytics.calculated_metrics` and display the mathematical breakdown ($Outcomes_i \times W_{species} \times W_{leverage} \times D_{evidence}$).
- [ ] 4.3 Add styling in Tailwind CSS to visually differentiate empirical extracted data from hardcoded EA constants.
- [ ] 4.4 Inject `{{ partial "ies-scorecard.html" $org }}` into `web/layouts/_default/single.html`.