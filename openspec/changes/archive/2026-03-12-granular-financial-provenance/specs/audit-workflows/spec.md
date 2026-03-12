## MODIFIED Requirements

### Requirement: Centralised Provenance Resolution Endpoint
The `utils_api` microservice SHALL provide a dedicated endpoint (e.g., `/resolve-provenance`) to programmatically convert raw LLM citations into exact, browser-routable deep links.

#### Scenario: Recursive Deep-Link Injection for Financials
- **WHEN** the Orchestrator passes the `financials` payload to the `/resolve-provenance` endpoint
- **THEN** it MUST transmit the entire, nested `financials` object rather than a flat array.
- **AND** the recursive `_find_and_resolve_sources` logic MUST automatically traverse the nested `income`, `expenditure`, and `reserves` objects, mutating and injecting the `resolved_url` for every discovered line-item source.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritized impact models, and highly traceable data provenance.

#### Scenario: Line-Item Financial Provenance Instructions
- **WHEN** generating system prompts for the Gemini model to extract financial data
- **THEN** the prompt MUST instruct the model to attach a specific `source` object to *every* extracted financial figure.
- **AND** the prompt MUST explicitly prohibit summarising sources into a top-level array, forcing the LLM to justify each extracted number (e.g., `income.donations.source`) with its exact, absolute page number and verifiable verbatim quote.