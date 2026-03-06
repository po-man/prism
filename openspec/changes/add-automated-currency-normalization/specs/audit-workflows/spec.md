# openspec/changes/add-automated-currency-normalization/specs/audit-workflows/spec.md

## ADDED Requirements

### Requirement: Orchestrator Exchange Rate Resolution
The n8n orchestrator SHALL dynamically resolve historical exchange rates to standardise financial data without modifying the raw extracted integers.

#### Scenario: Fetching Historical Year-End Rates
- **WHEN** the LLM successfully extracts the `financials` JSON payload
- **THEN** n8n MUST parse the `financial_year` string to isolate the primary reporting year (e.g., converting "2023-24" or "2023/2024" to "2023").
- **AND** n8n MUST execute an HTTP GET request to the Frankfurter API targeting December 31st of that parsed year (e.g., `https://api.frankfurter.dev/v1/2023-12-31?base=[original_code]&symbols=USD`).
- **AND** n8n MUST map the returned rate into the `financials.currency.usd_exchange_rate` field before passing the payload to the Data Vault and Utils API.
- **AND** if the `original_code` is already "USD", n8n MUST gracefully bypass the API call and set the rate to `1.0`.

## MODIFIED Requirements

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount, ensuring all cross-charity comparisons use a unified USD baseline.

#### Scenario: Calculating USD Cost per Outcome
- **WHEN** `check_cost_per_outcome` executes
- **THEN** it MUST multiply the raw `program_services_expenditure` by the `financials.currency.usd_exchange_rate` before dividing by the primary outcome.
- **AND** the resulting string MUST explicitly state the currency as USD (e.g., "($X USD / Y beneficiaries) = $Z USD per outcome. | A $1,000 USD donation achieves...").