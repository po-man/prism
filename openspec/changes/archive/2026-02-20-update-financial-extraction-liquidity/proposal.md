# Change: Update Financial Extraction for Liquidity Checks

## Why
Currently, the `check_liquidity` audit frequently returns a `null` status (Data Missing) for major NGOs (e.g., Watchdog Limited, HK Society for the Protection of Children). This occurs because the LLM struggles to find the explicit string "Net Current Assets" in the Annual Financial Reports (AFRs). If a donor sees "Data Missing" for fundamental financial health metrics on top-tier charities, they will lose trust in the platform's credibility. We need to build resilience into our extraction and calculation layers.

## What Changes
- **Schema Expansion:** Update `schemas/v1/financials.schema.json` to include `current_assets` and `current_liabilities` as optional fields under `ratio_inputs`.
- **Prompt Engineering:** Modify the decoupled prompt templates (`n8n/prompt-templates/financials.system.md` and `financials.user.md`) to explicitly instruct the LLM to look at the "Statement of Financial Position" or "Balance Sheet" to extract these raw component values if the net value isn't explicitly stated.
- **Fallback Logic:** Update the `check_liquidity` function in `utils_api/app/audits/financial.py`. If `net_current_assets` is missing, the system will attempt to calculate it dynamically using `current_assets - current_liabilities`.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`
- **Affected code:** - `schemas/v1/financials.schema.json`
  - `n8n/prompt-templates/financials.system.md`
  - `n8n/prompt-templates/financials.user.md`
  - `utils_api/app/audits/financial.py`
  - `utils_api/tests/test_audit.py`