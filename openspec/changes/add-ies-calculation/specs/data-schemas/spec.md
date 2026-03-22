## ADDED Requirements

### Requirement: Reference Data Collections for IES Constants
The system SHALL define static reference collections in PocketBase to store philosophical and epistemic constants, ensuring they are decoupled from individual charity records and can be updated globally.

#### Scenario: Storing EA Moral Weights and Evidence Discounts
- **WHEN** the system calculates the IES
- **THEN** it MUST reference a `ref_moral_weights` collection containing species-specific welfare capacities (e.g., `chicken: 0.1`).
- **AND** it MUST reference a `ref_evidence_discounts` collection containing epistemic penalty multipliers (e.g., `RCT: 1.0`, `Anecdotal: 0.1`).
- **AND** it MUST reference a `ref_intervention_baselines` collection for historical success probabilities of systemic interventions.

## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Extracting IES Empirical Variables
- **WHEN** validating the `impact.schema.json` and its corresponding extraction schema
- **THEN** the schema MUST strictly require the extraction of `species` (Beneficiary Category), `intervention_typology`, `evidence_claim` (methodology), and `raw_scale` ($Outcomes_{raw}$).
- **AND** if a value is not explicitly stated in the source document, the schema MUST enforce a `null` return to prevent LLM hallucinations.