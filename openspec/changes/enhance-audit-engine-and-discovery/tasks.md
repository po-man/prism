# openspec/changes/enhance-audit-engine-and-discovery/tasks.md

## 1. Schema Updates (`schemas`)
- [ ] 1.1 Update `schemas/v1/analytics.schema.json`: Add `"Data Transparency"` to the `enum` list for the `category` property.
- [ ] 1.2 Regenerate or test Pydantic models in `utils_api` to ensure they accept the new enum without breaking.

## 2. Audit Engine Additions (`utils_api`)
- [ ] 2.1 Create `utils_api/app/audits/transparency.py` and implement `check_financial_transparency`.
- [ ] 2.2 Create `utils_api/app/audits/risk.py` and implement `check_reputational_risk` mapping the risk payload to `pass/warning/fail`.
- [ ] 2.3 Register the new functions in `utils_api/app/audits/registry.py`.
- [ ] 2.4 Add unit tests for both new checks in `utils_api/tests/test_audit_transparency.py` and `test_audit_risk.py`.

## 3. UI / Hugo Updates (`web`)
- [ ] 3.1 Create `web/layouts/index.html` as the new landing page template.
- [ ] 3.2 Implement a Hugo `range` loop in `index.html` to iterate over `.Site.Data.organisations` and output a summary card for each.
- [ ] 3.3 Ensure summary cards include `data-risk`, `data-evidence`, and `data-beneficiary` HTML attributes.
- [ ] 3.4 Build `web/assets/js/filter.js` (or inline script) using Vanilla JS to handle button clicks that sort and filter the DOM elements based on EA metrics.
- [ ] 3.5 Add a top navigation bar to `baseof.html` to allow users to return to the landing page from individual report cards.