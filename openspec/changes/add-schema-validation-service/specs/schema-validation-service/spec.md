## MODIFIED Requirements

### Requirement: Master Governance Schema
The system SHALL utilize a set of strict, centralized JSON Schemas to validate all charity audit data. These schemas MUST be the single source of truth for data structure.

#### Scenario: Validating audit output
- **GIVEN** an AI agent has extracted data from a document for a specific domain (e.g., financials)
- **WHEN** the data is passed to the validation service
- **THEN** the service MUST load the corresponding schema from the `/schemas` directory (e.g., `schemas/v1/financials.schema.json`) to perform validation.
- **AND** the output MUST validate against that schema.