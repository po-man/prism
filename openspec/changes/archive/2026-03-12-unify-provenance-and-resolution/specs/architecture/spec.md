## MODIFIED Requirements

### Requirement: Separation of Concerns
The architecture SHALL strictly decouple orchestration, intelligence extraction, data validation, and frontend rendering.

#### Scenario: Centralising URL Resolution Logic
- **WHEN** unstructured references (like PDF page numbers or web search indices) need to be converted into clickable deep-links
- **THEN** this transformation MUST NOT occur within the Orchestrator (n8n) using inline JavaScript nodes.
- **AND** the Orchestrator MUST pass the raw extracted JSON and the necessary contextual URLs (report URLs and web search arrays) to a dedicated endpoint in the Logic layer (`utils_api`).
- **AND** the `utils_api` MUST deterministically construct and inject the `resolved_url` into every `source` object before it is persisted to the Data Vault.
