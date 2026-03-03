## MODIFIED Requirements

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