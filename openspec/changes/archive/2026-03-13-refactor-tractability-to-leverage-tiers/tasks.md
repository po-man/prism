# openspec/changes/refactor-tractability-to-leverage-tiers/tasks.md

## 1. Schema & Prompt Updates
- [x] 1.1 **Update Schema (`schemas/v1/impact.schema.json`)**:
  - Locate the `intervention_type` enum inside the `significant_events` items definition.
  - Expand the array to exactly these 13 values: `corporate_welfare_campaigns`, `policy_and_legal_advocacy`, `alternative_protein_and_food_tech`, `scientific_and_welfare_research`, `high_volume_spay_neuter`, `undercover_investigations_and_exposes`, `capacity_building_and_movement_growth`, `individual_rescue_and_sanctuary`, `veterinary_care_and_treatment`, `disaster_response_and_emergency_relief`, `wildlife_conservation_and_habitat_protection`, `vegan_outreach_and_dietary_change`, `humane_education_and_community_support`, `other`.
- [x] 1.2 **Update Prompt (`n8n/prompt-templates/impact.system.md`)**:
  - Replace the existing *Intervention Classification Rubric* with a new, comprehensive rubric detailing the 13 expanded types. 
  - Add definitions for the new types (e.g., `- alternative_protein_and_food_tech: Funding, researching, or promoting plant-based, precision-fermentation, or cultivated alternatives.`).
  - Instruct the LLM to prioritise specific categories over `other`.

## 2. Utils API Updates
- [x] 2.1 **Update Constants (`utils_api/app/audits/constants.py`)**:
  - Remove `INTERVENTION_TRACTABILITY_MAP`.
  - Add `INTERVENTION_LEVERAGE_MAP`. Key this dictionary by the 13 `intervention_type` strings.
  - For each key, assign a `tier` (integer 1, 2, or 3), a `tier_name` (e.g., "Tier 1: Systemic Change"), and a `note` containing the EA rationale.
- [x] 2.2 **Update Audit Logic (`utils_api/app/audits/impact.py`)**:
  - Rewrite `check_intervention_tractability(record: OrganisationRecord)`.
  - Filter `record.impact.significant_events` to only those with a valid `source.quote`.
  - Iterate through the verified events and group them by `tier_name` using `INTERVENTION_LEVERAGE_MAP`.
  - Determine the highest tier achieved overall (Tier 1 is highest priority). Set `base_item.details.calculation` to the highest `tier_name` found.
  - Assign status: `pass` if the highest tier is 1 or 2. `warning` if the highest tier is 3 or if no events are found.
  - Construct a structured portfolio dictionary. Format: `[{"tier_name": "Tier 1: Systemic Change", "interventions": [{"name": "Policy And Legal Advocacy", "source": {...}}]}]`. Serialize this dictionary to a JSON string and assign it to `base_item.details.elaboration`.
- [x] 2.3 **Update Tests (`utils_api/tests/test_audit_impact.py`)**:
  - Refactor `test_check_intervention_tractability` to mock events from the new 13-item taxonomy.
  - Assert that the output `status` correctly follows the Tier 1/2 (Pass) vs Tier 3 (Warning) logic.
  - Assert that `item["details"]["elaboration"]` is valid, parseable JSON containing the structured portfolio.

## 3. UI & Frontend Updates
- [x] 3.1 **Update Master Directory Columns (`web/layouts/index.html`)**:
  - Change the table header `<th>` from "Evidence Quality (Tractability)" to "Highest Leverage (Tractability)".
  - In the `<tbody>`, locate the `<td>` for Tractability. Extract the tier from `$tractabilityTier`. 
  - Render a visual badge using Tailwind classes (e.g., `bg-green-100 text-green-800` for Tier 1, `bg-yellow-100` for Tier 2, `bg-orange-100` for Tier 3, `bg-gray-100` for Not Assessed).
- [x] 3.2 **Update Sorting Logic (`web/layouts/index.html`)**:
  - Locate the `<script>` tag at the bottom.
  - Update the `if (sortType === 'tractability')` block. Map the string values to numeric weights for sorting: "Tier 1: Systemic Change" -> 3, "Tier 2: Preventative Scale" -> 2, "Tier 3: Direct Care" -> 1, "Not Assessed" -> 0.
- [x] 3.3 **Update Glossary (`web/layouts/partials/index-how-to-read.html`)**:
  - Change `data-highlight-column="Evidence Quality (Tractability)"` to match the new header.
  - Rewrite the explanatory `<p>` and `<ul>` to explain the Leverage Tiers (Systemic, Preventative, Direct Care) instead of RCTs/Anecdotal evidence.
- [x] 3.4 **Update Tractability Card (`web/layouts/partials/itn-scorecard.html`)**:
  - Locate the "Tractability" grid column. Change the sub-header to "Highest Intervention Leverage".
  - Refactor the `{{ if gt (len $tractabilityElaboration) 0 }}` block. 
  - Iterate over the unmarshaled `$tractabilityElaboration` array (which is now a structured portfolio of objects, not a list of strings).
  - For each tier group in the array, render a sub-heading (e.g., `<h4 class="text-sm font-bold text-gray-700 mt-3 border-b pb-1">Tier 1: Systemic Change</h4>`).
  - Loop through the `interventions` array within that tier group. For each intervention, render its name and immediately call `{{ partial "provenance-badge.html" .source }}` to attach the interactive citation.