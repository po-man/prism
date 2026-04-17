## Why
Currently, the LLM extraction pipeline struggles with financial tables that sequester unit multipliers (e.g., "in HK$ millions" or "in '000s") in table headers or footnotes. The model accurately extracts the raw tabular number (e.g., "20") but discards the contextual multiplier, resulting in severe, orders-of-magnitude errors in the database (recording $20 instead of $20,000,000). To maintain the strict "no-inference" extraction rule while resolving this mathematical anomaly, the system must structurally separate the raw number from its scale multiplier.

## What Changes
1. **Schema Expansion:** Introduce a `scale_multiplier` enum (`1`, `1000`, `1000000`) to the base financial figure definitions within `financials.schema.json`.
2. **Prompt Engineering:** Update the `financials.system.md` prompt to explicitly instruct the LLM to scan table headers and footnotes for scale keywords, extract the integer exactly as written into the `value` field, and apply the appropriate `scale_multiplier`.
3. **Audit Engine (`utils_api`):** Refactor the financial calculations (such as total expenditure and program service expenditure) to programmatically multiply the raw `value` by the `scale_multiplier` before applying any USD conversion or cost-per-outcome division.
4. **UI Refactoring (Hugo):** Update the financial tooltips in the Impact Pathway to reflect the scaled local currency, ensuring the raw extracted integer and its multiplier remain transparent to the user.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/financials.schema.json`, `n8n/prompt-templates/financials.system.md`, `utils_api/app/audits/impact.py`, `web/layouts/partials/impact-pathway.html`