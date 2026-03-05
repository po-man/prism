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

#### Scenario: Executing the data pipeline
- **WHEN** an evaluation pipeline runs
- **THEN** the Orchestrator (n8n) MUST manage the flow of data without executing complex business logic.
- **AND** the Intelligence layer (Gemini) MUST extract unstructured text into JSON without performing compliance threshold checks.
- **AND** the Logic layer (`utils_api`) MUST enforce JSON schemas and execute deterministic audit calculations.
- **AND** the Renderer (Hugo) MUST visualize the data without altering the underlying values or performing new calculations.

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