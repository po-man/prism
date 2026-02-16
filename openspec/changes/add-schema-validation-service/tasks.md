## 1. Schema Centralization

- [x] 1.1. Create a new versioned directory for schemas: `schemas/v1/`.
- [x] 1.2. Extract the `financials` JSON schema from the "Financials Prompts" node in `SUjUpjve9Vj6aJSbbuIWL.json` and save it as `schemas/v1/financials.schema.json`.
- [x] 1.3. Extract the `impact` JSON schema from the "Impact Prompts" node and save it as `schemas/v1/impact.schema.json`.
- [x] 1.4. Extract the `governance` JSON schema from the "Governance Prompts" node and save it as `schemas/v1/governance.schema.json`.
- [x] 1.5. Extract the `risk` JSON schema from the "Risk Prompts" node and save it as `schemas/v1/risk.schema.json`.
- [ ] 1.6. Archive the old `schemas/governance.schema.json` as it is now superseded by the more granular, up-to-date schemas.

## 2. Create Validation Service

- [x] 2.1. Set up a new Python project for the validation service (e.g., in a new `/utils_api` directory).
- [x] 2.2. Choose a web framework (e.g., FastAPI or Flask) and add it to the project's dependencies (`requirements.txt`).
- [x] 2.3. Implement a `/validate` endpoint that accepts `POST` requests.
  - [x] 2.3.1. The endpoint should accept a JSON body with two keys: `schema_name` (string, e.g., "v1/financials.schema.json") and `data` (the JSON object to validate).
  - [x] 2.3.2. The endpoint logic should load the specified schema file from the `/schemas` directory.
  - [x] 2.3.3. Use the `jsonschema` Python library to perform the validation.
  - [x] 2.3.4. If validation succeeds, return a `200 OK` response with `{"valid": true, ...}`.
  - [x] 2.3.5. If validation fails, return a `200 OK` response with a detailed error message, including the validation path and error type (e.g., `{"valid": false, "details": {...}, ...}`).
- [x] 2.4. Add basic error handling for cases where the schema file is not found.
- [x] 2.5. Create a `Dockerfile` for the new validation service to allow for containerization.
- [x] 2.6. Update the project's `docker-compose.yml` to include the new validation service.

## 3. Integrate Validation into n8n Workflow

This section focuses on modifying the `Charity Analysis` workflow (`SUjUpjve9Vj6aJSbbuIWL.json`).

- [x] 3.1. **Financials Validation:**
  - [x] 3.1.1. After the "Parsed Content (Financials)" node, add a new "HTTP Request" node named "Validate Financials Schema".
  - [x] 3.1.2. Configure it to `POST` to the new validation service's `/validate` endpoint.
  - [x] 3.1.3. The request body should be `{"schema_name": "v1/financials.schema.json", "data": {{ $('Parsed Content (Financials)').item.json.parsedContentObject }} }`.
  - [x] 3.1.4. Modify the "Storage API - Update Charity - Financials" node to save the extracted data and the validation result together. The payload for the `financials` field should be `{"data": {{...}}, "schema": {{...}} }`.

- [x] 3.2. **Impact Validation:**
  - [x] 3.2.1. After the "Parsed Content (Impact Metrics)" node, add a new "HTTP Request" node named "Validate Impact Schema".
  - [x] 3.2.2. Configure it to `POST` to the validation service with `schema_name: "v1/impact.schema.json"`.
  - [x] 3.2.3. Modify the "Storage API - Update Charity - Impact" node to save the extracted data and the validation result together.

- [x] 3.3. **Governance Validation:**
  - [x] 3.3.1. After the "Parsed Content (Governance Metrics)" node, add a new "HTTP Request" node named "Validate Governance Schema".
  - [x] 3.3.2. Configure it to `POST` to the validation service with `schema_name: "v1/governance.schema.json"`.
  - [x] 3.3.3. Modify the "Storage API - Update Charity - Governance" node to save the extracted data and the validation result together.

- [x] 3.4. **Risk Validation:**
  - [x] 3.4.1. After the "Parsed Content (Risk)" node, add a new "HTTP Request" node named "Validate Risk Schema".
  - [x] 3.4.2. Configure it to `POST` to the validation service with `schema_name: "v1/risk.schema.json"`.
  - [x] 3.4.3. Modify the "Storage API - Update Charity - Risk" node to save the extracted data and the validation result together.

## 4. Documentation and Testing

- [x] 4.1. Update `openspec/project.md` to mention the new validation service in the architecture section.
- [ ] 4.2. Create unit tests for the validation service, including tests for valid data, invalid data (e.g., missing required field, wrong type), and non-existent schemas.
- [x] 4.3. Manually run the updated n8n workflow to confirm that the validation steps work as expected for both success and failure cases.

## 5. Update Docker Configuration

- [x] 5.1. Modify the `docker-compose.yml` file (or equivalent deployment script). In the service definition for n8n, add a volume mount that maps the host's `./schemas` directory to a path inside the container, such as `/schemas`.
  ```yaml
  # Example for docker-compose.yml
  services:
    workflows:
      # ... other config
      volumes:
        - ./schemas:/schemas:ro # Mount as read-only
  ```

## 6. Refactor n8n Workflow (`SUjUpjve9Vj6aJSbbuIWL.json`)

For each data extraction block (Financials, Impact, Governance, Risk):

- [x] 6.1. **Financials:**
  - [x] 6.1.1. Before the "Financials Prompts" node, add a "Read File" node named "Read Financials Schema".
  - [x] 6.1.2. Configure it to read the file at path `/schemas/v1/financials.schema.json` and output the content as a string.
  - [x] 6.1.3. Modify the "Financials Prompts" node. In the `user_prompt`, replace the hardcoded JSON schema with an expression that injects the output from the "Read Financials Schema" node.

- [x] 6.2. **Impact:**
  - [x] 6.2.1. Add a "Read File" node for `/schemas/v1/impact.schema.json` before "Impact Prompts".
  - [x] 6.2.2. Update the "Impact Prompts" node to use the dynamically loaded schema.

- [x] 6.3. **Governance:**
  - [x] 6.3.1. Add a "Read File" node for `/schemas/v1/governance.schema.json` before "Governance Prompts".
  - [x] 6.3.2. Update the "Governance Prompts" node to use the dynamically loaded schema.

- [x] 6.4. **Risk:**
  - [x] 6.4.1. Add a "Read File" node for `/schemas/v1/risk.schema.json` before "Risk Prompts".
  - [x] 6.4.2. Update the "Risk Prompts" node to use the dynamically loaded schema.