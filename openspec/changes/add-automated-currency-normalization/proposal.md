# openspec/changes/add-automated-currency-normalization/proposal.md

## Why
As PRISM evaluates a Pan-Asian and global portfolio of animal advocacy charities, the extracted financial data is reported in diverse local currencies (e.g., HKD, INR, SGD). Comparing "Cost per Outcome" or total expenditures across these disparate currencies is impossible for Effective Altruism donors seeking a unified "Value for Money" baseline. We must normalise all financial metrics to USD while strictly preserving the raw extracted figures to ensure auditability and trust.

## What Changes
1. **Schema Expansion:** Add a `currency` object to `financials.schema.json` to store the original ISO 4217 currency code, the resolved USD exchange rate, and the date of the exchange rate.
2. **Prompt Engineering:** Instruct the LLM to identify and extract the local currency code from the financial reports.
3. **Orchestration (n8n):** Introduce an API integration with `frankfurter.dev`. n8n will parse the extracted `financial_year` (e.g., converting "2023-24" to "2023"), construct a query for December 31st of that year, and fetch the historical conversion rate to USD.
4. **Audit Engine (`utils_api`):** Refactor the `cost_per_outcome` logic to multiply the raw local expenditure by the stored USD exchange rate, outputting the final calculation and the "$1,000 donation" translation strictly in USD.
5. **UI Standardisation (Hugo):** Update all financial display components (Master Table, Impact Pathway, Value for Money) to dynamically calculate and render the USD equivalent, using tooltips to display the raw local currency for transparency.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/financials.schema.json`, `n8n/prompt-templates/financials.system.md`, `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`, `utils_api/app/audits/impact.py`, `web/layouts/partials/*`