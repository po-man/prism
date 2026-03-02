# openspec/changes/refactor-audit-checklist/proposal.md

## Why
The current `analytics` data model conflates deterministic audit checklist items (which should evaluate to Pass, Warn, or Fail) with pure informational calculations (e.g., Cost per Outcome, which currently uses a hacky `"null"` status). Additionally, the evaluation thresholds for financial and impact metrics lack a consistent warning tier, causing abrupt jumps between Pass and Fail. Finally, users lack immediate UI context regarding how these thresholds are determined. We must decouple calculations from compliance checks, standardize a three-tier evaluation logic, and introduce transparent UI tooltips.

## What Changes
1. **Schema Decoupling:** Update `analytics.schema.json` to introduce a separate `calculated_metrics` array. Remove the `"null"` status from `check_items.status`, enforcing strict `["pass", "fail", "warning"]` evaluations.
2. **Threshold Standardization (`utils_api`):** - *Liquidity:* Pass (>= 6 months), Warn (3 to < 6 months), Fail (< 3 months).
    - *Reserve Cap:* Pass (<= 2 years), Warn (> 2 and <= 5 years), Fail (> 5 years).
    - *Funding Neglectedness:* Pass (< 40%), Warn (40% to 80%), Fail (> 80%).
    - *Cause Area Neglectedness:* Pass (>= 50% high-neglectedness), Warn (> 0% to < 50%), Fail (0% high-neglectedness).
3. **Audit Engine Refactoring:** Move `check_cost_per_outcome` out of the `check_items` registry and into a dedicated metrics calculation pipeline in the Python API.
4. **UI Context & Tooltips (`web`):** Create a static dictionary in Hugo mapping each Audit ID to its threshold explanation. Render this as a hover tooltip on the frontend to explain *why* an item passed, warned, or failed. Update the "Value for Money" section to pull directly from the new `calculated_metrics` object.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/analytics.schema.json`, `utils_api/app/schemas/analytics.py`, `utils_api/app/audits/*`, `utils_api/app/routers/audit.py`, `web/layouts/partials/audit-checklist.html`, `web/layouts/partials/myth-buster.html`