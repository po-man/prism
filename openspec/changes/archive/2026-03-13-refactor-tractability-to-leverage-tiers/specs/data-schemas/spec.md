## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Expanded Intervention Taxonomy
- **WHEN** validating the `intervention_type` array within `significant_events`
- **THEN** the schema MUST support an expanded array of 13 specific intervention types designed to capture the full spectrum of animal advocacy leverage.
- **AND** the allowed enum MUST strictly be: `corporate_welfare_campaigns`, `policy_and_legal_advocacy`, `alternative_protein_and_food_tech`, `scientific_and_welfare_research`, `high_volume_spay_neuter`, `undercover_investigations_and_exposes`, `capacity_building_and_movement_growth`, `individual_rescue_and_sanctuary`, `veterinary_care_and_treatment`, `disaster_response_and_emergency_relief`, `wildlife_conservation_and_habitat_protection`, `vegan_outreach_and_dietary_change`, `humane_education_and_community_support`, and `other`.