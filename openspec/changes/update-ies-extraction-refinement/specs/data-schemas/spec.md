## MODIFIED Requirements

### Requirement: Reference Data Collections for IES Constants
The system SHALL define static reference collections in PocketBase to store philosophical and epistemic constants, ensuring they are decoupled from individual charity records and can be updated globally.

#### Scenario: Expanding Generic Species Fallbacks
- **WHEN** seeding or updating the `ref_moral_weights` collection
- **THEN** it MUST be populated with generic baseline records: `generic_companion`, `generic_farmed`, `generic_wild`, and `generic_unspecified`.
- **AND** the `ref_evidence_discounts` multipliers MUST be updated to reflect animal advocacy sector realities (e.g., `Pre-Post` adjusted to 0.6, `Anecdotal` to 0.3).

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Primary Intervention Designation
- **WHEN** validating the `significant_events.items.properties` within `impact_interventions.schema.json`
- **THEN** the schema MUST include a new `primary_intervention_type` field (string, referencing the intervention enum) alongside the existing `intervention_type` array, to prevent leverage inflation from secondary tags.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations, and qualifying calculations with confidence metadata.

#### Scenario: Dual IES Return Values
- **WHEN** validating the `iesMetric` definition within `analytics.schema.json`
- **THEN** it MUST be expanded to include both `claimed_ies` (integer, calculated without epistemic discounts) and `evaluated_ies` (integer, calculated with the $D_{evidence}$ multiplier applied).
- **AND** the `breakdown` array items MUST reflect both the claimed outcome score and the final evaluated score.