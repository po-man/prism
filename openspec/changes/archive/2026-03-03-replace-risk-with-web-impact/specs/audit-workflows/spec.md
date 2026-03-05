# openspec/changes/replace-risk-with-web-impact/specs/audit-workflows/spec.md

## ADDED Requirements

### Requirement: Document Ingestion Pipeline
The n8n orchestrator SHALL ingest target charities and their source documents, gracefully combining available PDFs with targeted web intelligence to maximize data extraction.

#### Scenario: Omni-Channel Impact Data Collection
- **WHEN** the primary analysis workflow is triggered and fetches charity data
- **THEN** it MUST dynamically construct and execute a web search query (e.g., `site:example.org (impact OR rescued OR animals OR annual OR report OR metrics)`) using the charity's official domain extracted during the metadata phase.
- **AND** it MUST aggregate the top search results into a clean `<web_context>` snippet string.
- **AND** the workflow MUST route to the Impact extraction branch if either an `annual_report` PDF exists OR the `domains` array is not empty (yielding web snippets).

## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations and maintaining strict data provenance.

#### Scenario: Reconciling PDF and Web Contexts
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the user prompt MUST distinctly separate the PDF text context and the injected `<web_context>`.
- **AND** the system prompt MUST instruct the model to prioritize data found in formal reports over web marketing copy if discrepancies exist.
- **AND** the system prompt MUST instruct the model that if a metric or event is extracted from the `<web_context>`, it MUST populate the corresponding `source_url` field with the URL provided in the snippet.
