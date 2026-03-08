## Why
Currently, PRISM calculates "Cost Per Outcome" by dividing total programme expenditure by the total quantified animal beneficiaries. This simplistic division suffers from a "Numerator-Denominator Mismatch" for charities that conduct significant non-animal work (e.g., human education, broad environmental policy). For these multi-domain charities, the numerator (total spend) includes non-animal costs, artificially inflating the cost per animal outcome. Presenting this skewed metric risks penalising highly effective systems-change organisations and misleading donors.

## What Changes
1. **Schema Expansion:** Update `impact.schema.json` to capture the charity's `operating_scope` (`pure_animal_advocacy` vs `multi_domain_operations`) and any explicitly stated unit costs. Expand `analytics.schema.json` metrics to include `confidence_tier` and `confidence_note`.
2. **Confidence-Tiered Logic:** Update the `utils_api` to evaluate "Cost Per Outcome" across three tiers:
   - **HIGH:** The charity explicitly states the unit cost in their reports (e.g., "$25 per dog").
   - **MEDIUM:** The charity is a pure animal advocacy organisation; PRISM calculates the unit cost via division.
   - **LOW:** The charity is multi-domain; the calculation is aborted (`null`) to prevent sticker shock and misrepresentation.
3. **UI Transparency:** Update the Master Directory to show "N/A" for Low Confidence items (sorted to the bottom) and display visual icons for High/Medium confidence. Update the individual profile to suppress the big number in Low Confidence scenarios, replacing it with an educational disclaimer.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/impact.schema.json`, `schemas/v1/analytics.schema.json`, `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/impact.py`, `web/layouts/index.html`, `web/layouts/partials/myth-buster.html`