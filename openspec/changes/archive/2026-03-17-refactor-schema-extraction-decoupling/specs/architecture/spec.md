## ADDED Requirements

### Requirement: Schema Decoupling for LLM Extraction
The architecture SHALL strictly decouple the canonical validation schemas used for data persistence from the lightweight extraction schemas injected into the LLM prompts. The validation schemas SHALL remain the Single Source of Truth (SSOT), whilst the extraction schemas MUST be programmatically derived build artifacts.

#### Scenario: Preventing FSM Compilation Bottlenecks
- **WHEN** the orchestrator triggers an LLM extraction node using the Gemini API
- **THEN** it MUST supply a compiled extraction schema rather than the canonical validation schema.
- **AND** this extraction schema MUST be stripped of high-cardinality state constraints (such as deep enums and strict URI formats) to prevent the LLM's finite state machine (FSM) compiler from throwing a "too many states for serving" error.
- **AND** the backend logic (`utils_api`) MUST reverse any schema-optimised transformations before performing final validation against the canonical SSOT schema.