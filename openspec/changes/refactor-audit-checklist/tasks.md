# openspec/changes/refactor-audit-checklist/tasks.md

## 1. Schema Refactoring (`schemas`)
- [x] 1.1 Update `schemas/v1/analytics.schema.json`:
  - Remove `"null"` from the `checkItem.status` enum.
  - Add a new definition for `calculatedMetric` (properties: `id`, `name`, `value`, `details`).
  - Add `calculated_metrics` (array of `calculatedMetric`) to the root properties, alongside `check_items`.

## 2. Python Audit Engine (`utils_api`)
- [x] 2.1 Refactor `app/schemas/analytics.py` to reflect the schema changes (create the `CalculatedMetric` model).
- [x] 2.2 Modify `app/audits/impact.py`:
  - Remove `check_cost_per_outcome` from returning an `AuditCheckItem`. Rewrite it to return a `CalculatedMetric`.
  - Update `check_funding_neglectedness` to return `fail` if ratio > 80% (instead of `warning`).
  - Update `check_cause_area_neglectedness` to return `fail` if high-neglectedness ratio == 0 (instead of `warning`).
- [x] 2.3 Modify `app/audits/financial.py`:
  - Update `check_reserve_cap`: `pass` <= 2, `warning` > 2 and <= 5, `fail` > 5.
  - Update `check_liquidity`: `pass` >= 6, `warning` >= 3 and < 6, `fail` < 3.
- [x] 2.4 Update `app/routers/audit.py` to route boolean checks to `check_items` and quantitative metrics to `calculated_metrics`.
- [x] 2.5 Update `tests/test_audit_financial.py` and `tests/test_audit_impact.py` to reflect the new three-tier boundaries and the new payload structure.

## 3. UI/UX Refactoring (`web`)
- [ ] 3.1 In `layouts/partials/audit-checklist.html`:
  - Create a local Hugo dictionary: `{{ $tooltips := dict "check_liquidity" "Pass: >=6 mos | Warn: 3-6 mos | Fail: <3 mos" "check_reserve_cap" "Pass: <=2 yrs | Warn: 2-5 yrs | Fail: >5 yrs" ... }}`.
  - Inject `title="{{ index $tooltips $item.id }}"` into the `<summary>` or icon container.
  - Remove the hacky `{{ if ne .status "null" }}` wrapper, as `check_items` will now strictly be booleans.
- [ ] 3.2 In `layouts/partials/myth-buster.html`:
  - Update the logic to fetch the cost per outcome from `$analytics.calculated_metrics` instead of ranging over `$analytics.check_items`.