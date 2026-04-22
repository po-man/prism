## ADDED Requirements

### Requirement: Document Ingestion Pipeline
The n8n orchestrator SHALL ingest target charities and their source documents, gracefully combining available PDFs with targeted web intelligence to maximize data extraction.

#### Scenario: Serialised Contextual Extraction for Impact Data
- **WHEN** the orchestrator triggers the Impact extraction phase
- **THEN** it MUST execute the extraction sub-domains sequentially in the following order: Beneficiaries $\rightarrow$ Interventions $\rightarrow$ Metrics $\rightarrow$ Transparency.
- **AND** for each subsequent step, the orchestrator MUST append the user prompts and the LLM's generated responses from all preceding steps into the `contents` array of the Gemini API payload, constructing a valid multi-turn chat history.
- **AND** this chat history MUST utilise the correct `"role": "user"` and `"role": "model"` structure to preserve the LLM's thought signature and ensure logical consistency across the charity's entire logic model.
- **AND** the workflow MUST consolidate the sequentially extracted JSON objects into a unified `impact.data` payload before persisting to the data vault.