# Proposal: CharityGrader Monorepo Skeleton

## Why
To achieve the project goal of "offline sovereignty," the system requires a rigid separation between data generation (auditing) and data presentation. A monolithic application would risk entangling the scraping logic with the viewing logic. By enforcing a file-system-based architecture from day one, we ensure:
1.  **Data Sovereignty:** The `data/` folder becomes the database, easily versioned via Git.
2.  **Schema Integrity:** A dedicated `schema/` directory acts as the single source of truth for both the backend (n8n) and frontend (Hugo).
3.  **Deployment Agility:** The frontend can be built and deployed independently of the heavy scraping infrastructure.

## What Changes
- **Architecture & Directory Structure**:
  - From: (Empty Repository)
  - To: A structured monorepo with distinct workspaces for `workflows` (n8n), `schemas` (JSON standards), `data` (audit artifacts), and `web` (Hugo SSG).

**Impact**
- **Breaking:** N/A (Initial commit).
- **Dependencies:** Requires Docker for n8n and Hugo for the web layer.