## MODIFIED Requirements

### Requirement: Impact Equivalency Score (IES) Processing Flow
The orchestration pipeline SHALL execute a rigid, multi-stage data lineage to compute the IES, ensuring every component of the calculation retains its traceability to source documents and accurately reflects species-specific moral weights.

#### Scenario: Resolving Species Weights via Text Expansion and Beneficiary Matching
- **WHEN** the `utils_api` computes the `w_species` for an IES metric
- **THEN** it MUST first search for a direct species key by evaluating a combined string of the metric's `unit`, `metric_name`, `context_qualifier`, and `source.quote`.
- **AND** if a direct species key is not found, it MUST attempt to link the metric to a specific demographic by fuzzy-matching the metric's text/quote against the quotes in the `beneficiaries` array.
- **AND** if a matching beneficiary record is found, it MUST apply the moral weight corresponding to that specific `beneficiary_type` (e.g., `generic_farmed`).
- **AND** it MUST ONLY fall back to the organisation-wide `dominant_beneficiary_type` if both the keyword search and the fuzzy beneficiary match fail.