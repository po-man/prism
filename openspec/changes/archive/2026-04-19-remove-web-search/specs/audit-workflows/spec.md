## REMOVED Requirements

### Requirement: Document Ingestion Pipeline
**Reason**: The omni-channel approach blending PDF and web data violated strict audit principles. The pipeline will now exclusively process attached PDF documents.
**Migration**: Remove all n8n nodes related to Google Search, search snippet aggregation, and web URL resolution.

## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations and maintaining strict data provenance.

#### Scenario: Enforcing Zero-Hallucination Constraints
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST NOT reference `<web_context>` or instruct the model to reconcile web snippets against PDF text.
- **AND** the prompt MUST strictly constrain the model to extract facts exclusively from the provided, audited document context.

### Requirement: Centralised Provenance Resolution Endpoint
The `utils_api` microservice SHALL provide a dedicated endpoint (e.g., `/resolve-provenance`) to programmatically convert raw LLM citations into exact, browser-routable deep links.

#### Scenario: Resolving PDF Provenance
- **WHEN** the Orchestrator passes the payload to the `/resolve-provenance` endpoint
- **THEN** the recursive `_find_and_resolve_sources` logic MUST ONLY process sources where `source_type` is `attached_report`.
- **AND** it MUST construct the `resolved_url` using the base document URL and the `#page=[page_number]` fragment.
- **AND** it MUST NOT attempt to resolve or append text fragments for web search URLs.