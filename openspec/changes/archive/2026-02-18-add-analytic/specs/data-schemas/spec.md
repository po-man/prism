# data-schemas Specification (Delta)

## MODIFIED Requirements
### Requirement: Master Governance Schema
The system SHALL utilize a set of strict, centralized JSON Schemas to validate all charity audit data. These schemas MUST be the single source of truth for data structure.

#### Scenario: Validating analytic output
- **GIVEN** the analytical engine has completed the check-item processing
- **WHEN** the results are passed to the validation service
- **THEN** the service MUST load `schemas/v1/analytics.schema.json` to perform validation.

## ADDED Requirements
### Requirement: Analytics Check-Item Schema
The system SHALL define a schema for the `analytics` field that captures the results of the pass/fail audit checklist.

#### Scenario: Validating a Check-Item Result
- **THEN** the schema MUST require the following properties for each item:
  - `id`: Unique slug (e.g., `check_reserve_cap`).
  - `status`: Enum `["pass", "fail", "warning", "null"]`.
  - `significance`: Enum `["HIGH", "MEDIUM", "LOW"]`.
  - `category`: Enum `["Financial Health", "Governance", "Impact Awareness", "Risk Management"]`.
  - `details`: Object containing `formula`, `calculation`, and `source_snippets`.

### Requirement: Formula Transparency
Every analytical check-item MUST provide the raw arithmetic used to reach its conclusion to ensure user-verifiability.

#### Scenario: Explaining the Reserve Ratio
- **WHEN** the `check_reserve_cap` fails
- **THEN** the `details.calculation` MUST stringify the values: `"($HKD 1,000,000 / $HKD 3,000,000) = 33.3% > 25% cap"`.