# openspec/changes/add-automated-currency-normalization/specs/data-schemas/spec.md

## MODIFIED Requirements

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons.

#### Scenario: Preserving Raw Currency and Exchange Rates
- **WHEN** the `financials.schema.json` is validated
- **THEN** the root of the schema MUST include a `currency` object.
- **AND** the `currency` object MUST contain `original_code` (string, ISO 4217 format), `usd_exchange_rate` (number), and `rate_date` (string, YYYY-MM-DD format).
- **AND** all values within the `income`, `expenditure`, and `reserves` objects MUST remain in the raw `original_code` denomination exactly as extracted from the source document.