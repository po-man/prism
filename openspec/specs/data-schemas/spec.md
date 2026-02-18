# data-schemas Specification

## Purpose
TBD - created by archiving change add-governance-schema. Update Purpose after archive.
## Requirements
### Requirement: Master Governance Schema
The system SHALL utilize a set of strict, centralized JSON Schemas to validate all charity audit data. These schemas MUST be the single source of truth for data structure.

#### Scenario: Validating analytic output
- **GIVEN** the analytical engine has completed the check-item processing
- **WHEN** the results are passed to the validation service
- **THEN** the service MUST load `schemas/v1/analytics.schema.json` to perform validation.

### Requirement: Traceability & Provenance
Every extracted data point MUST include a direct citation to its source to ensure auditability.

#### Scenario: Sourcing Financials
- **WHEN** the `total_annual_revenue` is recorded
- **THEN** it MUST be accompanied by a `source` object containing:
  - `url`: The direct link to the Annual Report PDF.
  - `page`: The page number (integer).
  - `snippet`: The exact text extracted (e.g., "Total Income: $45,200,300").

### Requirement: Financial Health Definitions
The schema SHALL enforce standard financial accounting definitions suitable for ratio analysis.

#### Scenario: Liquidity Inputs
- **WHEN** extracting balance sheet data
- **THEN** the schema MUST require `net_current_assets` and `monthly_operating_expenses`.

### Requirement: LSG Regulatory Compliance
The schema SHALL capture specific regulatory compliance flags mandated by the Social Welfare Department (SWD).

#### Scenario: LSG Reserve Compliance
- **WHEN** the charity is flagged as `lsg_subvented: true`
- **THEN** the schema MUST require the field `lsg_reserve_percent`.
- **AND** if `lsg_reserve_percent` > 25.0, a `compliance_warning` flag MUST be set to true.

### Requirement: Impact Evidence Standards
The schema SHALL structure impact data according to the "Hierarchy of Evidence" based on self-reported data.

#### Scenario: Grading Evidence Quality
- **WHEN** extracting impact data
- **THEN** the `evidence_quality` field MUST be an Enum restricted to:
  - `"RCT/Meta-Analysis"` (Gold standard)
  - `"Quasi-Experimental"` (Control groups used)
  - `"Pre-Post"` (Before/After comparison only)
  - `"Anecdotal"` (Stories/Testimonials only)
  - `"None"` (No data provided)

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

