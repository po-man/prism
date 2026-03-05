# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns and exact evidence citations.

#### Scenario: Animal Advocacy Metrics Extraction
- **WHEN** validating the impact data of an animal charity
- **THEN** the schema MUST support `beneficiary_type` enums specifically for `"companion_animals"`, `"farmed_animals"`, and `"wild_animals"`.
- **AND** the schema MUST support capturing `intervention_type` (e.g., `"direct_care"`, `"corporate_campaigns"`, `"policy_advocacy"`, `"dietary_change"`).
- **AND** the `metrics` array items MUST include an optional `evidence_quote` (string) field to capture the exact wording from the official source that justifies the assigned `evidence_quality` level.
- **AND** the `beneficiaries` array items MUST include an optional `portion_percentage` (number, 0-100) field to capture the relative proportion of that beneficiary group when absolute `population` counts are unavailable.

#### Scenario: Web-Sourced Data Provenance and Verifiability
- **WHEN** validating the impact data of an animal charity
- **THEN** the `metrics` array items MUST include an optional `source_url` (string, format: uri) field to capture the specific web URL if the metric was extracted from a web snippet.
- **AND** the `significant_events` array items MUST include an optional `source_url` (string, format: uri) field for the same provenance tracking purpose.
- **AND** the `significant_events` array items MUST include a new optional `source_quote` (string) field to capture the exact wording from the official source that justifies the event summary, enabling text-fragment highlighting.

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

