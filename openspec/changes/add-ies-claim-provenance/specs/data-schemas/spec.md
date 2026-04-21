## MODIFIED Requirements

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items and calculated metrics specific to Effective Altruism principles, supporting detailed elaborations and explicitly storing the data lineage used for evaluation.

#### Scenario: Propagating Metric Provenance to IES Breakdown
- **WHEN** validating the `analytics.schema.json` for the `impact_equivalency_score` metric
- **THEN** the items within the `details.breakdown` array MUST include an optional `source` object.
- **AND** this `source` object MUST support the standard provenance fields (`source_type`, `page_number`, `quote`, `resolved_url`) to enable the frontend to trace the high-level impact claim back to its origin.