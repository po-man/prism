## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Handling Ambiguous Beneficiary Types
- **WHEN** validating the `impact.schema.json`
- **THEN** the items within the `beneficiaries` array MUST support an extended enum for `beneficiary_type`: `["companion_animals", "farmed_animals", "wild_animals", "unspecified"]`.
- **AND** this allows the system to capture quantified populations where the exact taxonomy is not disclosed by the reporting organisation.