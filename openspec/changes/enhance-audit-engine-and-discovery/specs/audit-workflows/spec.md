## ADDED Requirements

### Requirement: Data Transparency Audit Logic
The `utils_api` SHALL programmatically evaluate the presence of verified source documents.

#### Scenario: Checking Financial Transparency
- **WHEN** the audit engine runs
- **THEN** it MUST execute a `check_financial_transparency` function.
- **AND** if the `financial_report` ID exists in the organisation payload, it MUST return `status: "pass"`.
- **AND** if it is missing or null, it MUST return `status: "fail"` with significance `HIGH`.

### Requirement: Reputational Risk Audit Logic
The `utils_api` SHALL programmatically evaluate the AI-extracted risk assessment.

#### Scenario: Checking Reputational Risk
- **WHEN** the audit engine runs
- **THEN** it MUST execute a `check_reputational_risk` function.
- **AND** evaluate `risk.data.overall_risk_level`. If `LOW`, return `pass`; if `MEDIUM`, return `warning`; if `HIGH`, return `fail` with significance `HIGH`.