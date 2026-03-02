# openspec/changes/update-asia-expansion-and-ui-refinements/specs/data-schemas/spec.md

## ADDED Requirements

### Requirement: Charity Metadata Schema
The system SHALL define a canonical JSON schema for extracting core identifying metadata applicable to charities worldwide, rather than restricted to a single jurisdiction.

#### Scenario: Pan-Asian Charity Extraction
- **WHEN** validating the metadata of an international charity
- **THEN** the schema MUST support a generalized `registration_id` field (replacing the HK-specific `s88_id`) to capture official non-profit identifiers globally.

## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns and exact evidence citations.

#### Scenario: Animal Advocacy Metrics Extraction
- **WHEN** validating the impact data of an animal charity
- **THEN** the schema MUST support `beneficiary_type` enums specifically for `"companion_animals"`, `"farmed_animals"`, and `"wild_animals"`.
- **AND** the schema MUST support capturing `intervention_type` (e.g., `"direct_care"`, `"corporate_campaigns"`, `"policy_advocacy"`, `"dietary_change"`).
- **AND** the `metrics` array items MUST include an optional `evidence_quote` (string) field to capture the exact wording from the official source that justifies the assigned `evidence_quality` level.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles in animal advocacy, supporting detailed elaborations.

#### Scenario: Audit Item Elaboration
- **WHEN** the audit engine generates the `check_items` array
- **THEN** the `details` object MUST include an optional `elaboration` field (string) to store exact-wording quotes or qualitative context that justifies non-calculation pass/fail statuses.