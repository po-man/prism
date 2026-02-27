## ADDED Requirements

### Requirement: Document Ingestion Pipeline
The n8n orchestrator SHALL ingest target charities and their source documents to begin the extraction process.

#### Scenario: Registry-Based Ingestion with Graceful Degradation
- **WHEN** the primary analysis workflow is triggered and fetches charity data
- **THEN** it MUST fetch a predefined list of HK animal charities and their document URLs from a PocketBase `registry` collection, bypassing the legacy SWD HTML scraper.
- **AND** the workflow MUST conditionally check for the existence of each document type (e.g., Impact Report, Financial Report).
- **AND** if a document type is missing, the workflow SHALL bypass that specific extraction branch and pass a `null` object to the `utils_api` without failing the overall execution.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs.

#### Scenario: EA Animal Impact Extraction
- **WHEN** generating prompts for Gemini 2.5
- **THEN** the system prompt MUST instruct the model to prioritize quantitative data regarding animal lives improved/spared, corporate cage-free commitments secured, or plant-based meals served.
- **AND** the prompt MUST strictly instruct the model to classify evidence quality according to the ITN framework.

## ADDED Requirements

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions tailored to animal advocacy.

#### Scenario: Evaluating Neglectedness
- **WHEN** the `utils_api` processes the `impact` data object
- **THEN** it MUST execute a `check_cause_area_neglectedness` function.
- **AND** if the `beneficiary_type` is `"farmed_animals"` or `"wild_animals"`, the status SHALL be `pass` (High Neglectedness).
- **AND** if the `beneficiary_type` is `"companion_animals"`, the status SHALL be `warning` (Low Neglectedness / Saturated space), reflecting EA resource allocation principles.