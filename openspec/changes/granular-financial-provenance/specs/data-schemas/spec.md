## MODIFIED Requirements

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons and granular data provenance.

#### Scenario: Enforcing Figure-Level Provenance
- **WHEN** the `financials.schema.json` is validated
- **THEN** the root of the schema MUST NOT contain a top-level `sources` array.
- **AND** a new definition called `financial_figure` MUST be created, comprising a `value` (number or null) and a `source` (referencing the unified source object, or null).
- **AND** all individual metrics within the `income`, `expenditure`, `reserves`, `lsg_specifics`, and `ratio_inputs` objects MUST strictly adhere to the `financial_figure` definition, enabling line-item attribution.