# System Architecture Specification

## Purpose
This specification defines the high-level directory structure, data flow, and separation of concerns for the CharityGrader system.

## ADDED Requirements

### Requirement: Monorepo Directory Structure
The project SHALL maintain a strict monorepo structure to separate orchestration, data definition, storage, and presentation.

#### Scenario: Initializing the repository
- **WHEN** the project is initialized
- **THEN** it SHALL contain the following top-level directories:
  - `workflows/`: Contains n8n workflow JSONs and embedded Python scripts.
  - `schemas/`: Contains JSON Schema definitions (e.g., `governance.schema.json`).
  - `data/`: The immutable data store for audit results (JSON format).
  - `web/`: The Hugo Static Site Generator source code.
  - `openspec/`: Project specifications and change management.

### Requirement: Schema Centralization
The `schemas/` directory SHALL serve as the single source of truth for data validation.

#### Scenario: Referencing schemas
- **WHEN** developing n8n workflows
- **THEN** the workflow must reference the schemas in `schemas/` for data validation nodes.
- **AND** the frontend build process MUST validate `data/` files against these schemas before generation.

### Requirement: Data Sovereignty
The `data/` directory SHALL function as the primary database.

#### Scenario: Storing audit results
- **WHEN** an audit workflow completes
- **THEN** it SHALL write the result as a `.json` file to `data/organisations/[id].json`.
- **AND** this file SHALL be committed to Git.

### Requirement: Frontend Independence
The `web/` directory SHALL contain only presentation logic and templates.

#### Scenario: Generating the site
- **WHEN** the build command is triggered (e.g., GitHub Actions)
- **THEN** Hugo SHALL ingest files from the `data/` directory.
- **AND** generate static HTML into a `public/` directory (which is git-ignored).