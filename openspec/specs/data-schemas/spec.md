# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Multi-Label Intervention Classification and Granular Taxonomy
- **WHEN** validating the `impact.schema.json`
- **THEN** the `significant_events.items.properties.intervention_type` MUST be defined as an `array` of strings, allowing multiple classifications per event.
- **AND** the array items MUST be restricted to the following expanded enum: `["corporate_welfare_campaigns", "policy_and_legal_advocacy", "high_volume_spay_neuter", "vegan_outreach_and_education", "individual_rescue_and_sanctuary", "veterinary_care_and_treatment", "capacity_building_and_grants", "other"]`.
- **AND** a new string property named `intervention_type_other_description` MUST be present to capture brief descriptions when "other" is selected.

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

