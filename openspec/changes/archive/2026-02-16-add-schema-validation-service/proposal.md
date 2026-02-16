# Change: Introduce Centralized Schema Validation Service

## Why
Currently, JSON schemas are defined inline within n8n workflow prompts, leading to a drift between the "source of truth" in the workflow and the formal schemas in the `/schemas` directory. There is also no automated validation step to ensure that data extracted by the LLM conforms to the required structure before it's persisted, which risks data corruption.

This change introduces a dedicated validation service to act as a gatekeeper, ensuring all data is schema-compliant before storage.

## What Changes
- **Architecture:** A new Python-based microservice (e.g., using FastAPI) will be created to provide schema validation via a REST API.
- **Schemas:** All schemas will be extracted from the n8n workflows and centralized in the `/schemas` directory, which will become the single source of truth. The existing `governance.schema.json` will be updated and potentially split into more granular schemas (financials, impact, etc.).
- **Workflows:** The `Charity Analysis` workflow (`SUjUpjve9Vj6aJSbbuIWL.json`) will be modified. Before each data extraction all to the Perplexity API, a new step will read the schema in order in construct the prompt. After each data extraction call to the Perplexity API, a new step will call the validation service. The workflow will only proceed to save the data to PocketBase if validation is successful.

## Impact
- **Affected Specs:**
  - `data-schemas`: Will be modified to reflect the new, centralized schema structure.
  - `architecture`: Will be modified to include the new validation service.
- **Affected Code:**
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`: Will be updated with new HTTP request nodes for validation.
  - `schemas/governance.schema.json`: Will be replaced or updated.
- **New Code:**
  - A new Python microservice for validation.
  - New schema files under `/schemas/`.