## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and operating scope context.

#### Scenario: Extracting Operating Scope and Explicit Unit Costs
- **WHEN** the `impact.schema.json` is validated
- **THEN** it MUST include a new root-level object named `context`.
- **AND** the `context` object MUST contain `operating_scope` with an enum of `["pure_animal_advocacy", "multi_domain_operations"]`.
- **AND** the `context` object MUST contain an optional `explicit_unit_cost` object containing `amount` (number), `currency` (string), and `description` (string) to capture costs explicitly declared by the charity.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations, and qualifying calculations with confidence metadata.

#### Scenario: Tiering Calculated Metrics
- **WHEN** the `analytics.schema.json` is validated
- **THEN** items within `calculated_metrics` MUST include `confidence_tier` (enum: `["HIGH", "MEDIUM", "LOW"]`) and `confidence_note` (string).
- **AND** the `value` property MUST allow `null` to accommodate aborted calculations in Low Confidence scenarios.