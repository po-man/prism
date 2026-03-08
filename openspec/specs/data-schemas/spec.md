# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and operating scope context.

#### Scenario: Extracting Operating Scope and Explicit Unit Costs
- **WHEN** the `impact.schema.json` is validated
- **THEN** it MUST include a new root-level object named `context`.
- **AND** the `context` object MUST contain `operating_scope` with an enum of `["pure_animal_advocacy", "multi_domain_operations"]`.
- **AND** the `context` object MUST contain an optional `explicit_unit_cost` object containing `amount` (number), `currency` (string), and `description` (string) to capture costs explicitly declared by the charity.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons.

#### Scenario: Preserving Raw Currency and Exchange Rates
- **WHEN** the `financials.schema.json` is validated
- **THEN** the root of the schema MUST include a `currency` object.
- **AND** the `currency` object MUST contain `original_code` (string, ISO 4217 format), `usd_exchange_rate` (number), and `rate_date` (string, YYYY-MM-DD format).
- **AND** all values within the `income`, `expenditure`, and `reserves` objects MUST remain in the raw `original_code` denomination exactly as extracted from the source document.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations, and qualifying calculations with confidence metadata.

#### Scenario: Tiering Calculated Metrics
- **WHEN** the `analytics.schema.json` is validated
- **THEN** items within `calculated_metrics` MUST include `confidence_tier` (enum: `["HIGH", "MEDIUM", "LOW"]`) and `confidence_note` (string).
- **AND** the `value` property MUST allow `null` to accommodate aborted calculations in Low Confidence scenarios.

### Requirement: Charity Metadata Schema
The system SHALL define a canonical JSON schema for extracting core identifying metadata applicable to charities worldwide, rather than restricted to a single jurisdiction.

#### Scenario: Pan-Asian Charity Extraction
- **WHEN** validating the metadata of an international charity
- **THEN** the schema MUST support a generalized `registration_id` field (replacing the HK-specific `s88_id`) to capture official non-profit identifiers globally.

