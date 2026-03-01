# openspec/changes/update-asia-expansion-and-ui-refinements/tasks.md

## 1. Schema Refactoring
- [x] 1.1 In `schemas/v1/meta.schema.json`, rename the `"s88_id"` property to `"registration_id"`. Update the description to reflect worldwide non-profit registration IDs.
- [x] 1.2 In `schemas/v1/impact.schema.json`, within the `metrics.items.properties` object, add an `"evidence_quote"` property (type: `["string", "null"]`, description: "The exact wording quoted from the official source justifying the evidence level."). Add it to the `required` array for metrics.
- [x] 1.3 In `schemas/v1/analytics.schema.json`, within `definitions.checkItem.properties.details.properties`, add an `"elaboration"` property (type: `["string", "null"]`).

## 2. Prompt Engineering (`n8n/prompt-templates`)
- [x] 2.1 In `meta.system.md`, update instructions to reflect a pan-Asian scope. Specifically mention extracting any official country/state non-profit registration ID (e.g., EIN, Charity Commission number, etc.) into the `registration_id` field.
- [x] 2.2 In `impact.system.md`, add the following instructions:
    - "You must extract the exact, verbatim sentence from the text that justifies the `evidence_quality` level and place it in the `evidence_quote` field."
    - "You must sort the `significant_events` and `metrics` arrays in descending order of significance. The interventions or metrics affecting the highest number of animals or driving the most systemic change must be placed first."

## 3. Python Audit Engine Updates (`utils_api`)
- [x] 3.1 Update `app/schemas/organisation.py` and `app/schemas/analytics.py` (No manual code changes needed if `create_dynamic_model` automatically pulls from the updated schemas, but ensure the server restarts to clear the `lru_cache`).
- [x] 3.2 In `app/audits/impact.py` -> `check_cost_per_outcome`:
    - Change the logic from `primary_outcome = max(all_outcomes)` to use the sum of beneficiaries.
    - Logic implementation: `primary_outcome = sum([b.population for b in record.impact.beneficiaries if b.population is not None])`.
    - If `primary_outcome` is 0, fallback to `sum([m.quantitative_data.value for m in record.impact.metrics if m.quantitative_data and m.quantitative_data.value is not None])`.
- [x] 3.3 In `app/audits/impact.py` -> `check_evidence_quality`:
    - Extract the `evidence_quote` associated with the metric that triggered the highest evidence level.
    - Assign this string to `base_item.details.elaboration = f"Quote: '{extracted_quote}'"` (ensure `AuditDetails` Pydantic model allows this instantiation dynamically, or update the model mapping).
- [x] 3.4 Update `tests/test_audit_impact.py` and `tests/test_validation.py` to reflect the new `registration_id`, `evidence_quote`, and `elaboration` schema properties, and adjust the math assertions for `check_cost_per_outcome` to expect summed values.

## 4. UI / Hugo Refactoring (`web`)
- [ ] 4.1 In `layouts/_default/single.html`: Update the `s88_id` reference to `registration_id` if it is rendered anywhere in the header.
- [ ] 4.2 In `layouts/partials/itn-scorecard.html`:
    - **Importance Card:** Modify the logic to print `$totalPop` instead of `$maxPop`. Below the `<p class="text-gray-600">Affects up to...`, iterate over `$sortedBeneficiaries` to print a small demographic breakdown list (e.g., `- 2,000 Wild Animals`, `- 500 Farmed Animals`).
    - **Tractability Card:** Fetch the highest evidence metric's `evidence_quote`. Render it below the evidence tier in an italicized blockquote or smaller text to elaborate on the evidence level.
- [ ] 4.3 In `layouts/partials/impact-pathway.html`:
    - Implement the "Top 3 Expandable" logic for the Activities array (`$impact.significant_events`).
    - Use `{{ $firstThree := first 3 $impact.significant_events }}` and `{{ $rest := after 3 $impact.significant_events }}`.
    - Render `$firstThree` unconditionally. 
    - If `$rest` has items, wrap them in a `<div x-show="expanded" style="display:none;" class="...">` (or use HTML `<details>`/vanilla JS if Alpine is not bundled) and provide a "Show all {{ len $impact.significant_events }} activities" toggle button.
    - Repeat the exact same Top 3 logic for the Outcomes array (`$impact.metrics`).
- [ ] 4.4 In `layouts/partials/myth-buster.html`:
    - Wrap the "Estimated Cost per Outcome" title or the text in a `<span title="Formula: Program Expenses / Sum of Beneficiaries">` to satisfy the tooltip requirement.
- [ ] 4.5 In `layouts/partials/audit-checklist.html`:
    - Within the `{{ range $sortedItems }}` loop, add an `{{ if ne $item.status "null" }}` condition to prevent calculation-only items (like Cost per Outcome) from rendering in the checklist.
    - Inside the `<details>` expansion block, add `{{ with $item.details.elaboration }}<p class="mt-2 text-sm text-gray-700 italic border-l-2 border-gray-300 pl-2">{{ . }}</p>{{ end }}` to render the exact wordings/elaborations.