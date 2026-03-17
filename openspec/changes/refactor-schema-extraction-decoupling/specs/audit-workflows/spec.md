## ADDED Requirements

### Requirement: Extraction Payload Reversal and Validation
The `utils_api` microservice SHALL intercept LLM extraction payloads and deterministically reverse any structural abbreviations applied during the extraction schema compilation phase before executing standard validation.

#### Scenario: Reversing Shortened Keys in `utils_api`
- **WHEN** the `utils_api` receives an unvalidated JSON payload from the orchestrator's extraction nodes
- **THEN** it MUST execute a recursive reversal function utilising the `key_mapping.json` artifact (or by dynamically reading `x-extract-key` definitions from the in-memory validation schema).
- **AND** it MUST safely swap all abbreviated keys (e.g., `other_desc`) back to their canonical long-form names (e.g., `intervention_type_other_description`).
- **AND** only after this structural restoration is complete SHALL the payload be passed to the `jsonschema.validate()` method against the canonical validation schema.

## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritised impact models, and highly traceable data provenance.

#### Scenario: Injecting Lightweight Schemas in n8n
- **WHEN** the "Prepare Prompts" sub-workflow executes the "Read JSON schema" nodes
- **THEN** it MUST target the newly generated extraction schemas (e.g., `impact.extract.schema.json`) located in the mounted schemas directory.
- **AND** the subsequent Gemini extraction nodes MUST use these lightweight schemas to guide the FSM, whilst relying on the modified `description` fields to enforce semantic classification and enum adherence.