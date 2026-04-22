## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, strictly enforcing the extraction of verbatim evidence and explicitly mapping metrics to global reference keys.

#### Scenario: Strict Metric Classification Keys
- **WHEN** validating the `impact_metrics.schema.json`
- **THEN** each metric MUST require a `species_key` and an `intervention_key` (both strings).
- **AND** these fields MUST conform to the exact enums injected dynamically by the orchestrator at runtime.

#### Scenario: Merging Self-Reported Evidence Types
- **WHEN** validating the `evidence_quality` of a metric
- **THEN** the allowed enum values MUST strictly be `["RCT/Meta-Analysis", "Quasi-Experimental", "Self-Reported"]`.
- **AND** any legacy unstructured or anecdotal evidence MUST be classified exclusively under `Self-Reported`.

### Requirement: Reference Data Collections for IES Constants
The system SHALL define static reference collections in PocketBase to store philosophical and epistemic constants, ensuring they are decoupled from individual charity records and can be updated globally.

#### Scenario: Pruning Out-of-Scope Moral Weights
- **WHEN** the `ref_moral_weights` collection is queried
- **THEN** it MUST NOT contain a `human` species key, enforcing the platform's strict focus on animal advocacy.

#### Scenario: Normalising Epistemic Discounts
- **WHEN** the `ref_evidence_discounts` collection is queried
- **THEN** it MUST return a single `Self-Reported` category with a unified penalty multiplier, eliminating the artificial distinction between `Pre-Post`, `Anecdotal`, and `None` for self-published charity reports.