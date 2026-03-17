# architecture Specification

## Purpose
This specification defines the overall system architecture, technology stack, and core technical conventions for PRISM. It outlines the strict separation of concerns between the orchestrator (n8n), intelligence layer (Gemini API), validation and logic microservice (utils_api), data vault (PocketBase), and renderer (Hugo). It also establishes project-wide conventions for data sovereignty and offline-first presentation.
## Requirements
### Requirement: Monorepo Directory Structure
The project SHALL maintain a strict monorepo structure to organize and isolate orchestration, API services, data definitions, and presentation logic.

#### Scenario: Initializing the repository
- **WHEN** the project is initialized or updated
- **THEN** it SHALL contain the following top-level directories:
  - `n8n/`: Contains n8n workflow JSONs, credentials, and Markdown prompt templates.
  - `utils_api/`: Contains the Python/FastAPI microservice for schema validation and deterministic audit logic.
  - `schemas/`: Contains JSON Schema definitions (e.g., `financials.schema.json`, `impact.schema.json`).
  - `pocketbase/`: Contains SQLite data and JavaScript migrations for the primary data vault.
  - `data/`: The secondary immutable data store for audit results (JSON format) ingested by the frontend.
  - `web/`: The Hugo Static Site Generator source code and Tailwind CSS configuration.
  - `openspec/`: Project specifications and change management proposals.

### Requirement: Separation of Concerns
The architecture SHALL strictly decouple orchestration, intelligence extraction, data validation, and frontend rendering.

#### Scenario: Centralising URL Resolution Logic
- **WHEN** unstructured references (like PDF page numbers or web search indices) need to be converted into clickable deep-links
- **THEN** this transformation MUST NOT occur within the Orchestrator (n8n) using inline JavaScript nodes.
- **AND** the Orchestrator MUST pass the raw extracted JSON and the necessary contextual URLs (report URLs and web search arrays) to a dedicated endpoint in the Logic layer (`utils_api`).
- **AND** the `utils_api` MUST deterministically construct and inject the `resolved_url` into every `source` object before it is persisted to the Data Vault.

### Requirement: Schema Centralization
The `schemas/` directory SHALL serve as the single source of truth for data validation across all services.

#### Scenario: Enforcing data contracts
- **WHEN** data is extracted by Gemini or processed by n8n
- **THEN** it MUST be sent to the `utils_api` `/validate` endpoint.
- **AND** the `utils_api` MUST strictly validate the payload against the corresponding canonical JSON schema in the `schemas/` directory before the data can be persisted.

### Requirement: Data Sovereignty and Persistence
The system SHALL utilize PocketBase as the primary source of truth, maintaining a secondary file-based export for the static frontend.

#### Scenario: Storing audit results
- **WHEN** an audit workflow completes successfully
- **THEN** it SHALL persist the structured entity (metadata, financials, impact, analytics) into the `organisations` collection in PocketBase.
- **AND** it SHALL subsequently export the record as an immutable JSON file to `data/organisations/[id].json`.
- **AND** it SHALL generate a routing Markdown stub at `web/content/[id].md` to enable Hugo page generation.

### Requirement: Frontend Independence (Offline-First)
The `web/` directory SHALL contain only presentation logic, producing a completely self-sufficient static build.

#### Scenario: Generating the static site
- **WHEN** the build command is triggered (e.g., via GitHub Actions)
- **THEN** Hugo SHALL ingest the local JSON files from the `data/` directory and Markdown stubs from `web/content/`.
- **AND** the generated HTML in the `public/` directory MUST NOT rely on any runtime API connections, external databases, or external CDNs (e.g., Google Fonts) for its core reporting functionality.

### Requirement: Schema Decoupling for LLM Extraction
The architecture SHALL strictly decouple the canonical validation schemas used for data persistence from the lightweight extraction schemas injected into the LLM prompts. The validation schemas SHALL remain the Single Source of Truth (SSOT), whilst the extraction schemas MUST be programmatically derived build artifacts.

#### Scenario: Preventing FSM Compilation Bottlenecks
- **WHEN** the orchestrator triggers an LLM extraction node using the Gemini API
- **THEN** it MUST supply a compiled extraction schema rather than the canonical validation schema.
- **AND** this extraction schema MUST be stripped of high-cardinality state constraints (such as deep enums and strict URI formats) to prevent the LLM's finite state machine (FSM) compiler from throwing a "too many states for serving" error.
- **AND** the backend logic (`utils_api`) MUST reverse any schema-optimised transformations before performing final validation against the canonical SSOT schema.

