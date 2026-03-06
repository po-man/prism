## 1. Schema Updates (`schemas`)
- [x] 1.1 In `schemas/v1/impact.schema.json`, add the `timeframe` property (enum: `["annual", "cumulative", "unspecified"]`) to the `metrics.items.properties` object. Add it to the `required` array for metrics.
- [x] 1.2 In `schemas/v1/impact.schema.json`, add the `timeframe` property to the `significant_events.items.properties` object. Add it to the `required` array for significant events.

## 2. Prompt Engineering (`n8n/prompt-templates`)
- [ ] 2.1 In `n8n/prompt-templates/impact.system.md`, add a new instruction for **Temporal Bounding**: "You must classify the timeframe of every metric and event. Use 'annual' if it occurred during the reporting year, 'cumulative' if it represents a total since inception or spanning multiple years, and 'unspecified' if it is unclear."
- [ ] 2.2 In `n8n/prompt-templates/impact.system.md`, update the **Disaggregated Populations** rule to enforce reconciliation: "The populations you assign in the `beneficiaries` array MUST represent the total number of animals helped *during the specific reporting year*. You must reconcile this total so that it logically aligns with the sum of the 'annual' metrics you extract. Do not use cumulative historical totals for the beneficiaries array."

## 3. Python Audit Engine (`utils_api`)
- [ ] 3.1 In `utils_api/app/audits/impact.py` -> `calculate_cost_per_outcome`, update the fallback logic for `primary_outcome` to strictly filter by timeframe:
  `primary_outcome = sum([m.quantitative_data.value for m in record.impact.metrics if m.quantitative_data and m.quantitative_data.value is not None and getattr(m, 'timeframe', '') == 'annual'])`.
- [ ] 3.2 In `utils_api/tests/test_audit_impact.py`, update `test_check_cost_per_outcome` to add a test case verifying that cumulative metrics are ignored when the fallback triggers.

## 4. UI / Hugo Refactoring (`web`)
- [ ] 4.1 In `web/layouts/partials/itn-scorecard.html`, locate the container `div` for the "Importance" card and the "Neglectedness" card.
- [ ] 4.2 Update the header area of these cards to use a flexbox layout to push the tag to the right (e.g., wrap the `<h3>` in a `<div class="flex justify-between items-start">`).
- [ ] 4.3 Inject the temporal tag: `<span class="text-[10px] font-mono uppercase tracking-wider text-gray-500 bg-gray-100 px-2 py-0.5 rounded border border-gray-200">Annual</span>` into the new flex container for both cards.