## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Enforcing Strict Taxonomy for Quantitative Metrics
- **WHEN** validating the `metrics` array within the `impact.schema.json`
- **THEN** the schema MUST require a new field `intervention_category` for each metric.
- **AND** this field MUST be strictly constrained to the existing EA intervention enum (e.g., `high_volume_spay_neuter`, `individual_rescue_and_sanctuary`, `veterinary_care_and_treatment`, `vegan_outreach_and_dietary_change`, `corporate_welfare_campaigns`, `policy_and_legal_advocacy`, `other`).
- **AND** this ensures that quantitative outcomes can be programmatically grouped and compared across different organisations.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons and granular data provenance.

#### Scenario: Capturing Line-Item Programme Costs
- **WHEN** validating the `expenditure` object within `financials.schema.json`
- **THEN** the schema MUST support an optional `granular_program_services` array.
- **AND** each item in this array MUST contain an `intervention_category` (using the identical EA enum from the impact schema) and a `cost` (which references the `financial_figure` definition).
- **AND** this allows the system to map specific financial expenditures directly to their corresponding impact metrics.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations, and qualifying calculations with confidence metadata.

#### Scenario: Storing a Sparse Matrix of Unit Costs
- **WHEN** validating the `calculated_metrics` array within `analytics.schema.json`
- **THEN** the schema MUST permit multiple `cost_per_outcome` objects, rather than a single monolithic metric.
- **AND** the `id` field for these metrics MUST support a composite string format (e.g., `cost_per_outcome:high_volume_spay_neuter`) to uniquely identify the intervention being costed.