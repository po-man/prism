## 1. Schema Updates
- [x] 1.1 Modify `schemas/v1/financials.schema.json`. Under `properties.ratio_inputs.properties`, add `current_assets` (type: number/null) and `current_liabilities` (type: number/null).

## 2. Extraction/Prompt Layer (LLM Prompts)
- [x] 2.1 Open `n8n/prompt-templates/financials.system.md`.
- [x] 2.2 Update the prompt instructions to include a directive: *"When looking for Net Current Assets, examine the Balance Sheet / Statement of Financial Position. If 'Net Current Assets' is not explicitly calculated, extract the total 'Current Assets' and 'Current Liabilities' so the system can calculate it."*
- [x] 2.3 Open `n8n/prompt-templates/financials.user.md` and ensure the field mapping instructions correctly reference the newly added schema fields (`current_assets` and `current_liabilities`).

## 3. Python Logic Layer (utils_api)
- [x] 3.1 In `utils_api/app/audits/financial.py`, update the `check_liquidity` function.
- [x] 3.2 Add conditional logic: 
      `if assets is None and getattr(record.financials.ratio_inputs, 'current_assets', None) is not None and getattr(record.financials.ratio_inputs, 'current_liabilities', None) is not None:`
      `assets = record.financials.ratio_inputs.current_assets - record.financials.ratio_inputs.current_liabilities`
- [x] 3.3 Ensure the `details.calculation` string correctly reflects whether the dynamic fallback was used (e.g., `"(($5,000,000 - $2,000,000) / $1,000,000) = 3.0 months"`).

## 4. Testing & Validation
- [x] 4.1 Update `utils_api/tests/test_validation.py` to include `current_assets` and `current_liabilities` in the mock `VALID_FINANCIALS` payload.
- [x] 4.2 Update `utils_api/tests/test_audit.py` to test the new fallback logic: pass a payload with missing `net_current_assets` but populated components, and assert `check_liquidity` returns a `pass` or `fail` instead of `null`.