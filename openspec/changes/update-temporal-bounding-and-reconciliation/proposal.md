## Why
Currently, PRISM's impact extraction pipeline is suffering from temporal data leakage. The web intelligence search frequently extracts "since inception" or cumulative figures (e.g., 11,000 total dogs rescued over 20 years). Because our system does not differentiate between annual and cumulative data, these lifetime figures are evaluated against a single year's financial expenditure. 

Furthermore, the LLM struggles to reconcile specific impact metrics (e.g., 8,422 medical treatments) with the overarching `beneficiaries` array (which it sometimes populates with arbitrary or heavily deflated numbers, such as 112). This combination produces extreme mathematical distortions in our EA "Value for Money" (Cost per Outcome) calculations.

## What Changes
1. **Schema Expansion:** Add a mandatory `timeframe` property (enum: `annual`, `cumulative`, `unspecified`) to the `metrics` and `significant_events` arrays in the `impact.schema.json`.
2. **Prompt Engineering:** Update the `impact.system.md` instructions. The LLM must be explicitly directed to classify the timeframe of all metrics and events. Crucially, it must be instructed to logically reconcile the `population` counts in the `beneficiaries` array to reflect the *annual* total of animals helped, matching the scale of the extracted annual metrics.
3. **Audit Engine Safeguard:** Refactor the `check_cost_per_outcome` fallback logic within `utils_api`. If it must rely on the `metrics` array to calculate outcomes, it must strictly filter for metrics where `timeframe == "annual"` to prevent dividing annual expenditure by a multi-decade cumulative impact metric.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`
- **Affected code:** `schemas/v1/impact.schema.json`, `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/impact.py`, `utils_api/tests/test_audit_impact.py`