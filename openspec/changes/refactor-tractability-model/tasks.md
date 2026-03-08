## 1. Schema Updates (`schemas/v1/`)
- [x] 1.1 In `impact.schema.json`, locate `significant_events.items.properties.intervention_type`.
- [x] 1.2 Change the `type` of `intervention_type` from `"string"` to `"array"`.
- [x] 1.3 Define the `items` of the array to be of type `"string"` with the `enum`: `["corporate_welfare_campaigns", "policy_and_legal_advocacy", "high_volume_spay_neuter", "vegan_outreach_and_education", "individual_rescue_and_sanctuary", "veterinary_care_and_treatment", "capacity_building_and_grants", "other"]`.
- [x] 1.4 Add a new property alongside `intervention_type` called `intervention_type_other_description` of type `["string", "null"]` with a max length constraint or description instructing a 3-5 word summary.

## 2. LLM Prompt Updates (`n8n/prompt-templates/`)
- [ ] 2.1 In `impact.system.md`, append a new section titled "**Intervention Classification Rubric**".
- [ ] 2.2 Add definitions for the LLM to use: 
  - `corporate_welfare_campaigns`: Pressuring/partnering with companies to adopt welfare policies.
  - `policy_and_legal_advocacy`: Lobbying governments or pursuing litigation for animal protection.
  - `high_volume_spay_neuter`: Catch-neuter-vaccinate-release (CNVR) and mass sterilisation.
  - `vegan_outreach_and_education`: Promoting dietary change to individuals via media or events.
  - `individual_rescue_and_sanctuary`: Direct rescue, sheltering, or rehoming of specific animals.
  - `veterinary_care_and_treatment`: Mobile clinics or hospitals treating owned/street animals.
  - `capacity_building_and_grants`: Funding or training other advocacy groups.
- [ ] 2.3 Add a strict instruction: "You may select multiple intervention types. If you must select 'other', you MUST provide a 3-5 word summary in the `intervention_type_other_description` field. Otherwise, leave it null."

## 3. Python Logic Updates (`utils_api/`)
- [ ] 3.1 Create `app/audits/constants.py`. Define the `INTERVENTION_TRACTABILITY_MAP` dictionary mapping the new enum keys to their EA evidence level (`"RCT/Meta-Analysis"`, `"Quasi-Experimental"`, `"Pre-Post"`, `"Anecdotal"`) and an explanatory `note`.
- [ ] 3.2 In `app/audits/impact.py`, rename the function `check_evidence_quality` to `check_monitoring_and_evaluation`. Update the ID, formula, and text inside the function to reflect M&E rather than general tractability.
- [ ] 3.3 In `app/audits/impact.py`, create a new function `check_intervention_tractability(record: OrganisationRecord) -> AuditCheckItem`.
- [ ] 3.4 Implement logic in `check_intervention_tractability`: Iterating over `record.impact.significant_events`, flattening the `intervention_type` arrays, mapping them to `INTERVENTION_TRACTABILITY_MAP`, and determining the highest tractability tier based on an internal hierarchy (RCT > Quasi > Pre-Post > Anecdotal). Set status to `pass` for RCT/Quasi, `warning` for lower. Populate `details.calculation` with the matched intervention and the EA rationale note.
- [ ] 3.5 In `app/audits/registry.py`, update `AUDIT_CHECKS` array to replace `check_evidence_quality` with `check_monitoring_and_evaluation` and append `check_intervention_tractability`.
- [ ] 3.6 Update `tests/test_audit_impact.py` to reflect the renamed M&E function and add unit tests for the new `check_intervention_tractability` function, testing single, multiple, and missing intervention mappings.

## 4. Hugo UI Updates (`web/layouts/`)
- [ ] 4.1 In `partials/itn-scorecard.html`, locate the "Tractability" card block.
- [ ] 4.2 Remove the existing Scratch logic that loops over `impact.data.metrics` to find the highest evidence and the `evidence_quote`.
- [ ] 4.3 Add logic to find the `check_intervention_tractability` item from `$analytics.check_items`.
- [ ] 4.4 Extract the highest evidence tier from the check's calculation/elaboration logic to display as the large text (replacing `$highestEvidence`).
- [ ] 4.5 Display the EA rationale string from `details.calculation` in the `<blockquote class="...">` section instead of the raw `evidence_quote`.
- [ ] 4.6 Ensure the "How to Read" modal in `partials/index-how-to-read.html` is updated to describe Tractability in terms of "EA Intervention Evidence Base" rather than "Self-Reported Evidence".