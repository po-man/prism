## MODIFIED Requirements
### Requirement: Schema Decoupling for LLM Extraction
The architecture SHALL strictly decouple the canonical validation schemas used for data persistence from the lightweight extraction schemas injected into the LLM prompts. The validation schemas SHALL remain the Single Source of Truth (SSOT), whilst the extraction schemas MUST be programmatically derived build artifacts. To maintain LLM focus and prevent hallucination, large monolithic extraction schemas MUST be split into modular, domain-specific sub-schemas to be executed concurrently.

#### Scenario: Preventing FSM Compilation Bottlenecks and Attention Degradation
- **WHEN** the orchestrator triggers an LLM extraction node using the Gemini API
- **THEN** it MUST supply a compiled, modular extraction schema rather than the canonical validation schema.
- **AND** for complex domains like Impact, the orchestrator MUST execute multiple concurrent LLM calls using split user prompts and sub-schemas (e.g., extracting beneficiaries separately from significant events).
- **AND** the backend logic (`utils_api`) MUST reverse any schema-optimised transformations before performing final validation against the canonical SSOT schema.

## ADDED Requirements
### Requirement: LLM Context Caching
The orchestrator SHALL utilise LLM-native context caching mechanisms to minimise redundant processing of large source artifacts across multiple extraction steps.

#### Scenario: Caching Multi-Document Analysis Batches
- **WHEN** the primary analysis workflow initiates extraction for an organisation
- **THEN** the orchestrator MUST verify if an active context cache exists in the Data Vault for the current analysis batch.
- **AND** if the cache is expired or missing, the orchestrator MUST construct a new cache payload combining the unified `master_auditor.system.md` prompt and the relevant PDF artifacts, storing the `cache_name` and `expire_time` in the Data Vault.
- **AND** all subsequent extraction nodes (Financials, Meta, Split Impact) MUST query this shared cache rather than re-uploading the documents.