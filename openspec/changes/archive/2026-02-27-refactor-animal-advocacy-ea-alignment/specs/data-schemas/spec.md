## ADDED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data.

#### Scenario: Animal Advocacy Metrics Extraction
- **WHEN** validating the impact data of an animal charity
- **THEN** the schema MUST support `beneficiary_type` enums specifically for `"companion_animals"`, `"farmed_animals"`, and `"wild_animals"`.
- **AND** the schema MUST support capturing `intervention_type` (e.g., `"direct_care"`, `"corporate_campaigns"`, `"policy_advocacy"`, `"dietary_change"`).

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data.

#### Scenario: Non-Subvented Charity Financials
- **WHEN** validating financial data for non-SWD charities
- **THEN** the schema MUST make `lsg_specifics` (Lump Sum Grant) optional or replace it with a generalized `reserves` object.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles in animal advocacy.

#### Scenario: Cause Area Neglectedness Check
- **WHEN** the audit engine generates the `check_items` array
- **THEN** it MUST include an item with ID `check_cause_area_neglectedness` that evaluates the tractability and neglectedness of the target species.