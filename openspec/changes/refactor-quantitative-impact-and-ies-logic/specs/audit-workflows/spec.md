## MODIFIED Requirements

### Requirement: Impact Equivalency Score (IES) Processing Flow
The orchestration pipeline SHALL execute a rigid, multi-stage data lineage to compute the IES, ensuring every component of the calculation retains its traceability to source documents and relies on explicitly assigned classifications rather than inferred string matching.

#### Scenario: Deterministic Reference Key Lookups
- **WHEN** the `utils_api` computes the `w_species`, `w_leverage`, and `d_evidence` for an IES metric
- **THEN** it MUST directly query the reference dictionaries using the `metric.species_key`, `metric.intervention_key`, and `metric.evidence_quality` extracted deterministically by the LLM.
- **AND** the pipeline MUST immediately bypass any fuzzy matching heuristics or substring overlap logic.
- **AND** if an exact match is not found in the reference tables, it MUST fall back to a predefined conservative baseline without attempting to infer context.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations and forcing the model to explicitly assign reference keys from the database.

#### Scenario: Dynamic Reference Enum Injection
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the orchestrator MUST dynamically fetch the live `species_key` and `intervention_key` lists from the Data Vault.
- **AND** it MUST inject these live lists into the JSON schema as strict enum constraints.
- **AND** the system prompt MUST instruct the model to evaluate the qualitative context of the metric and select the single most appropriate `species_key` and `intervention_key` from the provided enums.