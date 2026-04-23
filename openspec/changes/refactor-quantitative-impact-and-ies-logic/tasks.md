## 1. Database Migrations (`pocketbase/migrations/`)
- [x] 1.1 Create a new JS migration to delete the `human` record from the `ref_moral_weights` collection.
- [x] 1.2 In the same migration, remove the `None`, `Anecdotal`, and `Pre-Post` records from `ref_evidence_discounts`. Insert a new record: `{"evidence_key": "Self-Reported", "multiplier": 0.3, "description": "Self-reported claims without rigorous external control groups.", "source_citation": "PRISM Standard"}`.

## 2. Schema Refactoring (`schemas/`)
- [x] 2.1 In `schemas/v1/impact_metrics.schema.json` (and its `.extract` counterpart), update the `evidence_quality` enum to `["RCT/Meta-Analysis", "Quasi-Experimental", "Self-Reported"]`.
- [x] 2.2 Add `species_key` (type: string) and `intervention_key` (type: string) properties to the metric object.
- [x] 2.3 In `schemas/v1/impact_interventions.schema.json` (and its `.extract` counterpart), delete the `significant_events` array entirely, leaving only the `context` object.

## 3. n8n Orchestration Updates (`n8n/workflows/`)
- [x] 3.1 In `SUjUpjve9Vj6aJSbbuIWL.json`, add HTTP Request nodes to query PocketBase for all records in `ref_moral_weights`, `ref_evidence_discounts`, and `ref_intervention_baselines`.
- [x] 3.2 In the Code node preceding the Gemini Impact extraction, extract the keys from the PocketBase responses into Javascript arrays.
- [x] 3.3 Dynamically inject these arrays into the `enum` fields for `species_key`, `intervention_key`, and `evidence_quality` within the parsed `impact_metrics` schema object before passing it into the Gemini API call.

## 4. Python Audit Engine (`utils_api/`)
- [ ] 4.1 In `app/audits/impact.py`, locate `calculate_ies`.
- [ ] 4.2 Delete the `_fuzzy_match` helper function and all fuzzy matching logic within the metric loop.
- [ ] 4.3 Refactor the loop to retrieve the `w_species`, `w_leverage`, and `d_evidence` multipliers directly using `metric.species_key`, `metric.intervention_key`, and `metric.evidence_quality` from the reference dictionaries.
- [ ] 4.4 Update `tests/test_audit_impact.py` to reflect the new strict mapping and the removal of the fuzzy matching tests. Update mock data to use the "Self-Reported" evidence key.

## 5. UI/UX Refactoring (`web/`)
- [ ] 5.1 Delete `web/layouts/partials/impact-pathway.html`.
- [ ] 5.2 In `web/layouts/_default/single.html`, remove the `{{ partial "impact-pathway.html" $org }}` inclusion.
- [ ] 5.3 In `web/layouts/partials/itn-scorecard.html`, migrate the "What would happen without this charity?" (counterfactual) UI block from the deleted impact pathway, placing it directly beneath the "Impact Profile" header.
- [ ] 5.4 In `web/layouts/partials/myth-buster.html`, migrate the "Inputs" (Total Annual Expenditure) UI block from the deleted impact pathway, integrating it cleanly inside or above the "Expense Breakdown" column.