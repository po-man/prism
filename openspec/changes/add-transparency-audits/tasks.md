## 1. Schema Modifications (`schemas/`)
- [x] 1.1 Update `v1/analytics.schema.json`: Add `"bonus"`, `"not_disclosed"`, and `"n_a"` to the `status` enum in `checkItem`. Add `"Transparency"` to the `category` enum.
- [x] 1.2 Update `v1/impact.schema.json`: Add a `transparency_indicators` object containing `unintended_consequences_reported` and `euthanasia_statistics_reported`. Both should be objects containing a `value` (boolean) and a `$ref` to `#/definitions/source`.

## 2. LLM Prompt Updates (`n8n/prompt-templates/`)
- [ ] 2.1 Update `impact.system.md`: Add explicit instructions for the LLM to search for admissions of negative/unintended impacts and, if applicable, euthanasia/live release rates. Enforce that these must be backed by verbatim quotes, otherwise set the value to `false` and source to `null`.

## 3. Python Audit Engine (`utils_api/`)
- [ ] 3.1 Create `app/audits/transparency.py`.
- [ ] 3.2 Implement `check_negative_impact_disclosure(record)`. Returns `bonus` if `unintended_consequences_reported` is true, otherwise `not_disclosed`.
- [ ] 3.3 Implement `check_live_release_transparency(record)`. Check if `significant_events` contains rescue/veterinary interventions. If no, return `n_a`. If yes, check `euthanasia_statistics_reported`. Return `bonus` or `not_disclosed` accordingly.
- [ ] 3.4 Update `app/audits/registry.py` to import and append the two new checks to `AUDIT_CHECKS`.
- [ ] 3.5 Write unit tests in `tests/test_audit_transparency.py` to verify conditional logic and new statuses.

## 4. Frontend Updates (`web/`)
- [ ] 4.1 Update `layouts/partials/audit-checklist.html` styles: Add colour mapping for `bonus` (`bg-purple-100 text-purple-700`, `bg-purple-500` dot), `not_disclosed` (`bg-gray-100 text-gray-600`, `bg-gray-400` dot), and `n_a` (`bg-gray-100 text-gray-400`, empty/grey dot).
- [ ] 4.2 Update `layouts/partials/audit-checklist.html` text rendering: Map the raw string `"n_a"` to display as `"N/A"` and `"not_disclosed"` to display as `"NOT DISCLOSED"`, rather than relying on the default `upper` filter.
- [ ] 4.3 Update `layouts/partials/audit-checklist.html` sorting logic: Place `bonus` highest in the category block, and push `not_disclosed` and `n_a` to the bottom.