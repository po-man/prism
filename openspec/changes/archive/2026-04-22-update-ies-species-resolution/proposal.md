## Why
Currently, the Impact Equivalency Score (IES) calculation in the audit engine occasionally misassigns species weights (e.g., scoring cows as companion animals). This happens because the algorithm only searches the "unit" string for species keywords, and if not found, it falls back to the organisation's overall dominant beneficiary type. This skews the evaluated IES for multi-domain charities (e.g., those handling both companion and farmed animals) and undermines the accuracy of our EA tractability and neglectedness models.

## What Changes
- Expand the initial species keyword search in `calculate_ies` to scan a concatenated string of the metric's `unit`, `metric_name`, `context_qualifier`, and `source.quote`.
- Implement an intermediate fallback mechanism: attempt to fuzzy-match the metric's source quote against the quotes in the `beneficiaries` array. If a match is found, assign the specific `beneficiary_type` (mapped to `generic_<type>`) before resorting to the organisation-wide dominant type.

## Impact
- **Affected specs:** `audit-workflows`
- **Affected code:** - `utils_api/app/audits/impact.py`
  - `utils_api/tests/test_audit_impact.py`