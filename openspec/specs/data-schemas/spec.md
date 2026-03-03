# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns and exact evidence citations.

#### Scenario: Web-Sourced Data Provenance
- **WHEN** validating the impact data of an animal charity
- **THEN** the `metrics` array items MUST include an optional `source_url` (string) field to capture the specific web URL if the metric was extracted from a web snippet.
- **AND** the `significant_events` array items MUST include an optional `source_url` (string) field for the same provenance tracking purpose.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data.

#### Scenario: Non-Subvented Charity Financials
- **WHEN** validating financial data for non-SWD charities
- **THEN** the schema MUST make `lsg_specifics` (Lump Sum Grant) optional or replace it with a generalized `reserves` object.

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

