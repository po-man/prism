## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Enforcing Currency Standards and Nullability for Unit Costs
- **WHEN** validating the `explicit_unit_cost` object within `impact.context`
- **THEN** the `currency` field MUST explicitly demand a 3-letter ISO 4217 code to prevent ambiguous symbol usage.
- **AND** the internal properties (`amount`, `currency`, `description`) MUST accept `null` values to gracefully handle missing data without triggering strict validator failures or hallucinated zeroes.
- **AND** both `operating_scope` and `explicit_unit_cost` MUST include a `source` object property referencing the unified provenance schema.