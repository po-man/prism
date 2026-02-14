## 1. Schema Centralization

- [ ] 1.1. Create a new versioned directory for schemas: `schemas/v1/`.
- [ ] 1.2. Extract the `financials` JSON schema from the "Financials Prompts" node in `SUjUpjve9Vj6aJSbbuIWL.json` and save it as `schemas/v1/financials.schema.json`.
- [ ] 1.3. Extract the `impact` JSON schema from the "Impact Prompts" node and save it as `schemas/v1/impact.schema.json`.
- [ ] 1.4. Extract the `governance` JSON schema from the "Governance Prompts" node and save it as `schemas/v1/governance.schema.json`.
- [ ] 1.5. Extract the `risk` JSON schema from the "Risk Prompts" node and save it as `schemas/v1/risk.schema.json`.
- [ ] 1.6. Archive the old `schemas/governance.schema.json` as it is now superseded by the more granular, up-to-date schemas.

## 2. Create Validation Service

- [ ] 2.1. Set up a new Python project for the validation service (e.g., in a new `/services/validator` directory).
- [ ] 2.2. Choose a web framework (e.g., FastAPI or Flask) and add it to the project's dependencies (`requirements.txt`).
- [ ] 2.3. Implement a `/validate` endpoint that accepts `POST` requests.
  - [ ] 2.3.1. The endpoint should accept a JSON body with two keys: `schema_name` (string, e.g., "v1/financials.schema.json") and `data` (the JSON object to validate).
  - [ ] 2.3.2. The endpoint logic should load the specified schema file from the `/schemas` directory.
  - [ ] 2.3.3. Use the `jsonschema` Python library to perform the validation.
  - [ ] 2.3.4. If validation succeeds, return a `200 OK` response with `{"status": "valid"}`.
  - [ ] 2.3.5. If validation fails, return a `400 Bad Request` response with a detailed error message, including the validation path and error type (e.g., `{"status": "invalid", "error": "...", "path": "..."}`).
- [ ] 2.4. Add basic error handling for cases where the schema file is not found.
- [ ] 2.5. Create a `Dockerfile` for the new validation service to allow for containerization.
- [ ] 2.6. Update the project's `docker-compose.yml` to include the new validation service.

## 3. Integrate Validation into n8n Workflow

This section focuses on modifying the `Charity Analysis` workflow (`SUjUpjve9Vj6aJSbbuIWL.json`).

- [ ] 3.1. **Financials Validation:**
  - [ ] 3.1.1. After the "Parsed Content (Financials)" node, add a new "HTTP Request" node named "Validate Financials Schema".
  - [ ] 3.1.2. Configure it to `POST` to the new validation service's `/validate` endpoint.
  - [ ] 3.1.3. The request body should be `{"schema_name": "v1/financials.schema.json", "data": {{ $('Parsed Content (Financials)').item.json.parsedContentObject }} }`.
  - [ ] 3.1.4. Add an "If" node after the validation call to check if the status code is `200`.
  - [ ] 3.1.5. Connect the `true` branch of the "If" node to the "Storage API - Update Charity - Financials" node.
  - [ ] 3.1.6. Connect the `false` branch to an error-handling node (e.g., log the error and stop).

- [ ] 3.2. **Impact Validation:**
  - [ ] 3.2.1. After the "Parsed Content (Impact Metrics)" node, add a new "HTTP Request" node named "Validate Impact Schema".
  - [ ] 3.2.2. Configure it to `POST` to the validation service with `schema_name: "v1/impact.schema.json"`.
  - [ ] 3.2.3. Add a corresponding "If" node to gate the "Storage API - Update Charity - Impact" step.

- [ ] 3.3. **Governance Validation:**
  - [ ] 3.3.1. After the "Parsed Content (Governance Metrics)" node, add a new "HTTP Request" node named "Validate Governance Schema".
  - [ ] 3.3.2. Configure it to `POST` to the validation service with `schema_name: "v1/governance.schema.json"`.
  - [ ] 3.3.3. Add a corresponding "If" node to gate the "Storage API - Update Charity - Governance" step.

- [ ] 3.4. **Risk Validation:**
  - [ ] 3.4.1. After the "Parsed Content (Risk)" node, add a new "HTTP Request" node named "Validate Risk Schema".
  - [ ] 3.4.2. Configure it to `POST` to the validation service with `schema_name: "v1/risk.schema.json"`.
  - [ ] 3.4.3. Add a corresponding "If" node to gate the "Storage API - Update Charity - Risk" step.

## 4. Documentation and Testing

- [ ] 4.1. Update `openspec/project.md` to mention the new validation service in the architecture section.
- [ ] 4.2. Create unit tests for the validation service, including tests for valid data, invalid data (e.g., missing required field, wrong type), and non-existent schemas.
- [ ] 4.3. Manually run the updated n8n workflow to confirm that the validation steps work as expected for both success and failure cases.