## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, and temporal bounding.

#### Scenario: Temporal Bounding of Metrics and Events
- **WHEN** validating the impact data of a charity
- **THEN** the `metrics` array items MUST include a required `timeframe` (string) field with allowed enum values of `["annual", "cumulative", "unspecified"]` to prevent historical data from skewing annual financial ratios.
- **AND** the `significant_events` array items MUST include the same `timeframe` field to clearly distinguish between current-year activities and historical milestones.