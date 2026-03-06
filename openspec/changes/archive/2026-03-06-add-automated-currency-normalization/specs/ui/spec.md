# openspec/changes/add-automated-currency-normalization/specs/ui/spec.md

## MODIFIED Requirements

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, normalising all financial inputs to USD to prevent user confusion.

#### Scenario: Rendering Normalized Inputs
- **WHEN** rendering the "Inputs" card (Total Annual Expenditure)
- **THEN** the Hugo template MUST dynamically multiply the raw total expenditure by the `usd_exchange_rate`.
- **AND** it MUST render the value with a "USD" prefix (e.g., "USD $50,000").
- **AND** it MUST include a hover tooltip indicating the original local currency amount and the exchange rate used (e.g., "Original: HKD $390,000 (Rate: 0.128 as of 2023-12-31)").

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis.

#### Scenario: USD-Unified Cost per Outcome
- **WHEN** rendering the "Cost per Outcome" column in the Master Table
- **THEN** the UI MUST render the value extracted from `calculated_metrics`, which is now strictly guaranteed by the audit engine to be in USD.
- **AND** the column header MUST be explicitly labelled "Cost per Outcome (USD)".