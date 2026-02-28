## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns.

#### Scenario: Animal Advocacy Metrics Extraction
- **WHEN** validating the impact data of an animal charity
- **THEN** the schema MUST support `beneficiary_type` enums specifically for `"companion_animals"`, `"farmed_animals"`, and `"wild_animals"`.
- **AND** the schema MUST support capturing `intervention_type` (e.g., `"direct_care"`, `"corporate_campaigns"`, `"policy_advocacy"`, `"dietary_change"`).
- **AND** the `beneficiaries` array items MUST include an optional `portion_percentage` (number, 0-100) field to capture the relative proportion of that beneficiary group when absolute `population` counts are unavailable.