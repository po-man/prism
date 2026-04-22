## Why
Currently, a discrepancy exists between the Hugo UI and the `utils_api` Audit Engine regarding counterfactual baselines. The Audit Engine assigns an outright "Fail" if a strict numerical `value` is missing, even if a qualitative narrative is provided. However, simply allowing any `quote` to pass as a qualitative baseline introduces a critical vulnerability: the LLM often populates the quote field with denial statements (e.g., "No counterfactual provided") when data is absent. We must introduce a "Warning" tier for genuine qualitative baselines while rigorously filtering out false-positive denial statements.

## What Changes
1. **Prompt Engineering:** Update `impact.system.md` to strictly forbid the use of filler text (e.g., "N/A", "Not found") in quote fields, enforcing strict `null` outputs for missing data.
2. **Audit Logic Refactoring:** Update `check_counterfactual_baseline` in `utils_api/app/audits/impact.py` to evaluate both quantitative and qualitative baselines.
3. **Heuristic Sanitisation:** Introduce a validation helper in the audit engine to intercept quotes containing denial phrases or lacking sufficient character length, ensuring only genuine qualitative narratives trigger the "Warning" tier.

## Impact
- **Affected specs:** `audit-workflows`
- **Affected code:** `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/impact.py`, `utils_api/tests/test_audit_impact.py`