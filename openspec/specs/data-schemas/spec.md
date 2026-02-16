# data-schemas Specification

## Purpose
TBD - created by archiving change add-governance-schema. Update Purpose after archive.
## Requirements
### Requirement: Master Governance Schema
The system SHALL utilize a set of strict, centralized JSON Schemas to validate all charity audit data. These schemas MUST be the single source of truth for data structure.

#### Scenario: Validating audit output
- **GIVEN** an AI agent has extracted data from a document for a specific domain (e.g., financials)
- **WHEN** the data is passed to the validation service
- **THEN** the service MUST load the corresponding schema from the `/schemas` directory (e.g., `schemas/v1/financials.schema.json`) to perform validation.
- **AND** the output MUST validate against that schema.

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

