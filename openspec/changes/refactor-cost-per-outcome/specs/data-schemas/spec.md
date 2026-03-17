## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Extracting Multiple Explicit Unit Costs
- **WHEN** validating the `context` object within `impact.schema.json`
- **THEN** the schema MUST define `explicit_unit_costs` as an array of objects, rather than a single object.
- **AND** each object in the array MUST contain an `intervention_type` field referencing the `InterventionTypeEnum` to link the cost to a specific EA cause area.
- **AND** each object MUST retain the `amount`, `currency`, `description`, and `source` fields to ensure strict provenance.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons and granular data provenance.

#### Scenario: Extracting Programmatic Financial Breakdowns
- **WHEN** validating the `expenditure` object within `financials.schema.json`
- **THEN** the schema MUST include a `program_breakdowns` array.
- **AND** this array MUST accept objects containing `programme_name` (string) and `amount` (referencing the `financial_figure` definition).
- **AND** this allows the system to capture granular line-item spending (e.g., "Mobile Spay Clinic Operations: $50,000") beyond the aggregated `program_services` total.