# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions tailored to animal advocacy, extracting verifiable elaborations.

#### Scenario: Populating Audit Elaborations
- **WHEN** executing non-calculation audit functions (e.g., `check_evidence_quality`, `check_cause_area_neglectedness`)
- **THEN** the `utils_api` MUST populate the `details.elaboration` field with the corresponding `evidence_quote` from the source data, or generate a human-readable explanation of why the status was assigned.

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome based on cumulative impact and additionally provide a normalized translation for a standard retail donation amount ($1,000).

#### Scenario: Appending Retail Translation using Cumulative Outcomes
- **WHEN** `check_cost_per_outcome` successfully executes
- **THEN** the function MUST calculate the total primary outcome by summing all valid `population` integers in the `beneficiaries` array.
- **AND** it MUST calculate the cost per outcome by dividing the `program_services_expenditure` by this cumulative sum.
- **AND** it MUST append the translation to the `base_item.details.calculation` string (e.g., "... per outcome. | A $1,000 donation achieves ≈ X outcomes.").

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations.

#### Scenario: EA Animal Impact Extraction
- **WHEN** querying via LLM
- **THEN** the system prompt MUST instruct the model to prioritize quantitative data regarding animal lives improved/spared.
- **AND** the prompt MUST instruct the model to explicitly extract the exact `population` count for *each* `beneficiary_type` if the charity serves multiple categories of animals.
- **AND** the prompt MUST strictly instruct the model to classify evidence quality according to the ITN framework.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts and prioritized impact models.

#### Scenario: Extracting Pan-Asian Metadata and Sorted Impact
- **WHEN** generating prompts for the Gemini model
- **THEN** the metadata system prompt MUST instruct the model to locate any official government non-profit registration ID globally, mapping it to `registration_id`.
- **AND** the impact system prompt MUST instruct the model to extract exact verbatim sentences as `evidence_quote` to justify evidence quality.
- **AND** the impact system prompt MUST instruct the model to sort the `significant_events` and `metrics` arrays in descending order of significance or scale of impact.

