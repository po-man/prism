## ADDED Requirements

### Requirement: Centralised Provenance Resolution Endpoint
The `utils_api` microservice SHALL provide a dedicated endpoint (e.g., `/resolve-provenance`) to programmatically convert raw LLM citations into exact, browser-routable deep links.

#### Scenario: Resolving PDF Deep Links
- **WHEN** the `utils_api` receives a payload containing a `source` object where `source_type` is `annual_report` or `financial_report`
- **THEN** it MUST read the corresponding base URL provided in the request context.
- **AND** it MUST append `#page=N` to the URL (where N is the `page_number` integer).
- **AND** it MUST assign this concatenated string to the `resolved_url` field.

#### Scenario: Resolving Web Text Fragments
- **WHEN** the `utils_api` receives a payload containing a `source` object where `source_type` is `web_search`
- **THEN** it MUST locate the correct URL and original snippet from the provided `web_search_results` context array using the `search_result_index`.
- **AND** it MUST generate a W3C Text Fragment (`#:~:text=...`) using the `quote` string.
- **AND** it MUST assign the combined URL and fragment to the `resolved_url` field.

## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritized impact models, and highly traceable data provenance.

#### Scenario: Enforcing Absolute PDF Page Indexing
- **WHEN** generating system prompts for the Gemini model to extract data from PDFs
- **THEN** the prompt MUST explicitly instruct the LLM to populate the `source` object's `page_number` field using the **1-based absolute PDF page index**.
- **AND** the prompt MUST strictly instruct the LLM to ignore any printed page numbers found in the document's headers or footers (e.g., Roman numerals, "Page 2 of 50"), as these will break browser PDF routing.
- **AND** the prompt MUST instruct the LLM to extract exact verbatim sentences into the `quote` field of the `source` object for all data points.