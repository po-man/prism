# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, and temporal bounding.

#### Scenario: Temporal Bounding of Metrics and Events
- **WHEN** validating the impact data of a charity
- **THEN** the `metrics` array items MUST include a required `timeframe` (string) field with allowed enum values of `["annual", "cumulative", "unspecified"]` to prevent historical data from skewing annual financial ratios.
- **AND** the `significant_events` array items MUST include the same `timeframe` field to clearly distinguish between current-year activities and historical milestones.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons.

#### Scenario: Preserving Raw Currency and Exchange Rates
- **WHEN** the `financials.schema.json` is validated
- **THEN** the root of the schema MUST include a `currency` object.
- **AND** the `currency` object MUST contain `original_code` (string, ISO 4217 format), `usd_exchange_rate` (number), and `rate_date` (string, YYYY-MM-DD format).
- **AND** all values within the `income`, `expenditure`, and `reserves` objects MUST remain in the raw `original_code` denomination exactly as extracted from the source document.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations.

#### Scenario: Enforcing Strict Boolean Audits and Decoupling Calculations
- **WHEN** the `analytics.schema.json` is validated
- **THEN** the `check_items.items.properties.status` enum MUST ONLY allow `["pass", "fail", "warning"]`. The `"null"` value MUST be removed.
- **AND** the root of the schema MUST include a new array property named `calculated_metrics` alongside `check_items`.
- **AND** items within `calculated_metrics` MUST include `id` (string), `name` (string), `value` (number or string), and `details` (object containing `formula` and `calculation`).

### Requirement: Charity Metadata Schema
The system SHALL define a canonical JSON schema for extracting core identifying metadata applicable to charities worldwide, rather than restricted to a single jurisdiction.

#### Scenario: Pan-Asian Charity Extraction
- **WHEN** validating the metadata of an international charity
- **THEN** the schema MUST support a generalized `registration_id` field (replacing the HK-specific `s88_id`) to capture official non-profit identifiers globally.

