## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Multi-Label Intervention Classification and Granular Taxonomy
- **WHEN** validating the `impact.schema.json`
- **THEN** the `significant_events.items.properties.intervention_type` MUST be defined as an `array` of strings, allowing multiple classifications per event.
- **AND** the array items MUST be restricted to the following expanded enum: `["corporate_welfare_campaigns", "policy_and_legal_advocacy", "high_volume_spay_neuter", "vegan_outreach_and_education", "individual_rescue_and_sanctuary", "veterinary_care_and_treatment", "capacity_building_and_grants", "other"]`.
- **AND** a new string property named `intervention_type_other_description` MUST be present to capture brief descriptions when "other" is selected.