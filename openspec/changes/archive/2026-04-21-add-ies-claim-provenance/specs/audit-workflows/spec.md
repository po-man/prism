## MODIFIED Requirements

### Requirement: Impact Equivalency Score (IES) Processing Flow
The orchestration pipeline SHALL execute a rigid, multi-stage data lineage to compute the IES, ensuring every component of the calculation retains its traceability to source documents.

#### Scenario: Mapping Source Lineage for IES Metrics
- **WHEN** the `utils_api` computes the breakdown for the IES metric
- **THEN** the function MUST map the `metric.source` object from the ingested impact payload directly into the top-level `source` field of the corresponding breakdown item in the output analytics schema.