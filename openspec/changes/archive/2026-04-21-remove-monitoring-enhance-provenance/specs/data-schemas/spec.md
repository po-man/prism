## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, strictly enforcing the extraction of verbatim evidence over LLM-synthesised summaries.

#### Scenario: Counterfactual Baseline Provenance
- **WHEN** validating the `impact_metrics.schema.json`
- **THEN** the `counterfactual_baseline` object MUST include a `source` object.
- **AND** the `source` object MUST contain an optional `url` (string, uri format) and a required `quote` (string) field to store the exact text fragment justifying the baseline.
- **AND** the legacy `description` field MUST be deprecated to prevent structural hallucinations.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, supporting detailed elaborations and explicitly storing the criteria used for evaluation.

#### Scenario: Storing Evaluation Thresholds
- **WHEN** validating the `analytics.schema.json`
- **THEN** the `details` object within the `checkItem` definition MUST include a `criteria` field (string).
- **AND** this field MUST be used by the Python Audit Engine to pass the static Pass/Warn/Fail rules down to the frontend UI.