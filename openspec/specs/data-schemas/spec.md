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

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data.

#### Scenario: Non-Subvented Charity Financials
- **WHEN** validating financial data for non-SWD charities
- **THEN** the schema MUST make `lsg_specifics` (Lump Sum Grant) optional or replace it with a generalized `reserves` object.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles in animal advocacy, supporting detailed elaborations.

#### Scenario: Audit Item Elaboration
- **WHEN** the audit engine generates the `check_items` array
- **THEN** the `details` object MUST include an optional `elaboration` field (string) to store exact-wording quotes or qualitative context that justifies non-calculation pass/fail statuses.

### Requirement: Charity Metadata Schema
The system SHALL define a canonical JSON schema for extracting core identifying metadata applicable to charities worldwide, rather than restricted to a single jurisdiction.

#### Scenario: Pan-Asian Charity Extraction
- **WHEN** validating the metadata of an international charity
- **THEN** the schema MUST support a generalized `registration_id` field (replacing the HK-specific `s88_id`) to capture official non-profit identifiers globally.

