## 1. Schema Refactoring (`schemas/`)
- [x] 1.1 In `schemas/v1/impact_metrics.schema.json`, locate the `counterfactual_baseline` object. Delete the `description` string property.
- [x] 1.2 In the same object, add a `source` property referencing a new or existing provenance object containing `quote` (string) and `url` (string, nullable).
- [x] 1.3 In `schemas/v1/analytics.schema.json`, locate `definitions.checkItem.properties.details.properties`. Add a `"criteria"` property (type: `["string", "null"]`).

## 2. Python Audit Engine (`utils_api/`)
- [x] 2.1 Open `utils_api/app/audits/registry.py` and remove `check_monitoring_and_evaluation` from the `AUDIT_CHECKS` list.
- [x] 2.2 Open `utils_api/app/audits/impact.py`. Delete the `check_monitoring_and_evaluation` function entirely.
- [x] 2.3 In `utils_api/app/audits/impact.py`, iterate through every remaining `check_*` function. Update the instantiation of the `AuditDetails` Pydantic model to include the new `criteria` field. (e.g., `criteria="Pass: >= 50% High-Neglect Species | Warn: 1-49% | Fail: 0%"`).
- [x] 2.4 In `check_counterfactual_baseline`, extract `record.impact.counterfactual_baseline.source.quote` and assign it to `base_item.details.elaboration = f"Quote: '{extracted_quote}'"`.
- [x] 2.5 Open `utils_api/tests/test_audit_impact.py`. Delete tests related to M&E. Update remaining tests to expect the `criteria` string in the output dictionary and the modified counterfactual elaboration.

## 3. Hugo UI Refactoring (`web/layouts/partials/`)
- [x] 3.1 Open `web/layouts/partials/impact-pathway.html`.
- [x] 3.2 Locate the "What would happen without this charity?" section. Change the template variable from `.description` to `.source.quote`.
- [x] 3.3 Inject the `provenance-badge.html` partial next to the quote, passing in the `.source.url` and `.source.quote` to generate the W3C Text Fragment link.
- [x] 3.4 Open `web/layouts/partials/audit-checklist.html`.
- [x] 3.5 Delete the hardcoded `$tooltips` Hugo dictionary and remove the `title` attributes from the checklist rows.
- [x] 3.6 Inside the `<details>` expansion block, completely restructure the HTML.
    - Create a top section `div` with classes like `bg-gray-50 border border-gray-100 rounded p-3 mb-3 text-sm`. Add a bold header "Evaluation Criteria:" followed by `{{ $item.details.criteria }}`.
    - Create a bottom section `div` for the result. Render `{{ $item.details.calculation }}`.
    - Ensure `{{ $item.details.elaboration }}` is rendered below the calculation as an italicised blockquote with a left border (`border-l-4 border-gray-300 pl-3 italic`).