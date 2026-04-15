# openspec/changes/update-ies-extraction-refinement/tasks.md

## 1. PocketBase Data Architecture
- [ ] 1.1 Insert new baseline records into the `ref_moral_weights` collection (or update migration scripts) for: `generic_companion`, `generic_farmed`, `generic_wild`, and `generic_unspecified`, assigning EA-consensus median moral weights.
- [ ] 1.2 Update the `ref_evidence_discounts` collection/migrations to adjust multipliers (e.g., raising `Pre-Post` to 0.6 and `Anecdotal` to 0.3) to better reflect sector realities.

## 2. Schema Updates (`schemas/v1/`)
- [ ] 2.1 In `impact_interventions.schema.json`, add a `primary_intervention_type` string field (using the `InterventionTypeEnum`) to the `SignificantEvent` object to designate the core driver of the event.
- [ ] 2.2 In `analytics.schema.json`, update the `IesMetric` definition. Rename the `value` field (or add adjacent fields) to support `claimed_ies` and `evaluated_ies`. Update the `BreakdownItem` to include `claimed_ies_i`.
- [ ] 2.3 Run `scripts/generate_extraction_schemas.py` to compile the new extraction schemas for the LLM.

## 3. Prompt Engineering (`n8n/prompt-templates/`)
- [ ] 3.1 In `impact.system.md`, append the strict zero-hallucination constraints:
    - Explicitly mandate the inclusion of egg counts as valid biological beneficiaries.
    - Add strict negative constraints against extracting "potential/capacity" numbers and financial/currency figures as outcome/beneficiary counts.
    - Clarify that human-facing advocacy and education programs do not trigger the `multi_domain_operations` flag unless core budget is diverted.

## 4. Python Audit Engine (`utils_api/`)
- [ ] 4.1 In `utils_api/app/audits/impact.py`, implement a pre-processing filter in `calculate_ies` to exclude any metric where `timeframe != 'annual'`.
- [ ] 4.2 In `calculate_ies`, implement the bounding check: sum the `outcome.value` of all filtered annual metrics. If this exceeds the total annual `beneficiaries`, calculate a `bounding_ratio = total_beneficiaries / total_metric_outcomes` and apply this multiplier to each metric's outcome value.
- [ ] 4.3 Refactor the Metric-to-Event matching logic in `calculate_ies` to use fuzzy string matching (e.g., converting both to lowercase and checking for significant word overlap) instead of exact substring matching. If a match fails, assign the metric to a conservative fallback leverage probability instead of skipping it entirely.
- [ ] 4.4 Update the leverage multiplier logic to map strictly to the new `primary_intervention_type` field, bypassing the max-array iteration.
- [ ] 4.5 Refactor the species mapping in `calculate_ies` to query the new `generic_*` keys from PocketBase when an exact biological match isn't found.
- [ ] 4.6 Update the IES return object to supply both `claimed_ies` (calculated with $D_{evidence} = 1.0$) and `evaluated_ies` (incorporating $D_{evidence}$).
- [ ] 4.7 Update `tests/test_audit_impact.py` to verify the dual IES return, the bounding cap logic, and the fuzzy matching.

## 5. UI / Hugo Refactoring (`web/`)
- [ ] 5.1 In `web/layouts/partials/ies-scorecard.html`, restructure the UI to present "Claimed IES" prominently.
- [ ] 5.2 Add a sub-component (e.g., a badge or progress bar style element) titled "Epistemic Confidence Rating" that illustrates the $D_{evidence}$ discount.
- [ ] 5.3 Display the final "Evaluated IES" as the definitive bottom-line EA score.
- [ ] 5.4 Update the breakdown table to display both the claimed row score and the evaluated row score for full transparency.