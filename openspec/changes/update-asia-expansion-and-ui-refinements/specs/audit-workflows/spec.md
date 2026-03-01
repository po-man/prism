# openspec/changes/update-asia-expansion-and-ui-refinements/specs/audit-workflows/spec.md

## MODIFIED Requirements

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome based on cumulative impact and additionally provide a normalized translation for a standard retail donation amount ($1,000).

#### Scenario: Appending Retail Translation using Cumulative Outcomes
- **WHEN** `check_cost_per_outcome` successfully executes
- **THEN** the function MUST calculate the total primary outcome by summing all valid `population` integers in the `beneficiaries` array.
- **AND** it MUST calculate the cost per outcome by dividing the `program_services_expenditure` by this cumulative sum.
- **AND** it MUST append the translation to the `base_item.details.calculation` string (e.g., "... per outcome. | A $1,000 donation achieves ≈ X outcomes.").

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions tailored to animal advocacy, extracting verifiable elaborations.

#### Scenario: Populating Audit Elaborations
- **WHEN** executing non-calculation audit functions (e.g., `check_evidence_quality`, `check_cause_area_neglectedness`)
- **THEN** the `utils_api` MUST populate the `details.elaboration` field with the corresponding `evidence_quote` from the source data, or generate a human-readable explanation of why the status was assigned.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts and prioritized impact models.

#### Scenario: Extracting Pan-Asian Metadata and Sorted Impact
- **WHEN** generating prompts for the Gemini model
- **THEN** the metadata system prompt MUST instruct the model to locate any official government non-profit registration ID globally, mapping it to `registration_id`.
- **AND** the impact system prompt MUST instruct the model to extract exact verbatim sentences as `evidence_quote` to justify evidence quality.
- **AND** the impact system prompt MUST instruct the model to sort the `significant_events` and `metrics` arrays in descending order of significance or scale of impact.