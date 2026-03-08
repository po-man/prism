## 1. Schema Updates (`schemas/v1/`)
- [x] 1.1 In `impact.schema.json`, add a `context` object at the root level containing:
  - `operating_scope`: string, enum `["pure_animal_advocacy", "multi_domain_operations"]`.
  - `explicit_unit_cost`: object (nullable) containing `amount` (number), `currency` (string), and `description` (string).
- [x] 1.2 In `analytics.schema.json`, update `calculatedMetric` definition:
  - Add `confidence_tier`: string, enum `["HIGH", "MEDIUM", "LOW"]`.
  - Add `confidence_note`: string.
  - Modify `value` to be `["number", "string", "null"]`.

## 2. LLM Prompt Updates (`n8n/prompt-templates/`)
- [x] 2.1 In `impact.system.md`, add a strict instruction: "You must assess the charity's overall operations. If they focus purely on animals, set `operating_scope` to `pure_animal_advocacy`. If they also invest heavily in human education, climate change, or humanitarian aid, set it to `multi_domain_operations`."
- [x] 2.2 In `impact.system.md`, add an instruction: "If the charity explicitly states the exact cost to help an animal or deliver an intervention (e.g., 'It costs $25 to spay a dog'), capture this in `explicit_unit_cost`. Do NOT attempt to calculate this yourself."

## 3. Python Logic Updates (`utils_api/app/audits/`)
- [x] 3.1 In `impact.py`, update `calculate_cost_per_outcome` to fetch `record.impact.context`.
- [x] 3.2 Implement **HIGH Confidence** logic: If `explicit_unit_cost` exists, fetch the financial exchange rate matching the explicit currency (or default to 1.0 if USD). Multiply `amount` by the exchange rate. Set `value` to this amount, `confidence_tier` to `HIGH`, and append the high-confidence note.
- [x] 3.3 Implement **LOW Confidence** logic: If `explicit_unit_cost` is null AND `operating_scope` is `multi_domain_operations`, set `value` to `None`, `confidence_tier` to `LOW`, and append the multi-domain disclaimer note.
- [x] 3.4 Implement **MEDIUM Confidence** logic: If `explicit_unit_cost` is null AND `operating_scope` is `pure_animal_advocacy`, perform the existing calculation (Program Services USD / Total Beneficiaries). Set `confidence_tier` to `MEDIUM` and append the calculated disclaimer note.
- [x] 3.5 Update `tests/test_audit_impact.py` to cover High, Medium, and Low scenarios, verifying that the new `confidence_tier` and `confidence_note` fields populate correctly and that `value` is correctly nulled out for multi-domain charities.

## 4. Hugo UI Updates (`web/layouts/`)
- [x] 4.1 In `index.html` (Master Directory), update the "Cost per Outcome (USD)" column `<td>` generation:
  - Extract `confidence_tier` and `confidence_note`.
  - Set `data-sort-value` to the numeric value if HIGH/MEDIUM, or `-Infinity` if LOW.
  - If LOW: Render `<span class="text-gray-400" title="{{ confidence_note }}">N/A</span>`.
  - If HIGH: Render the formatted amount with a solid checkmark SVG (`title="{{ confidence_note }}"`).
  - If MEDIUM: Render the formatted amount with a calculator SVG (`title="{{ confidence_note }}"`).
- [x] 4.2 In `partials/myth-buster.html` (Individual Profile), locate the "Estimated Cost per Outcome" card.
  - Extract the `confidence_tier` and `confidence_note`.
  - Implement a `{{ if eq $confidence_tier "LOW" }}` block. Inside, hide the large number and retail translation. Render a visually distinct, subdued box containing the `confidence_note`.
  - Implement the `{{ else }}` block to show the standard large number and retail translation, but append an italicized `<p>` tag at the bottom of the card displaying the `confidence_note` for full transparency.