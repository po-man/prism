# audit-workflows Specification

## Purpose
TBD - created by archiving change add-audit-workflows. Update Purpose after archive.
## Requirements
### Requirement: Idempotent Execution & State Persistence
The system SHALL employ a checkpointing strategy to ensure that high-cost operations are not repeated unnecessarily.

#### Scenario: Analytical Re-run
- **WHEN** raw data (financials/governance) exists in PocketBase
- **AND** only the audit logic in `utils_api` has changed
- **THEN** the system MUST be able to re-run the analytics phase without re-extracting data from PDFs.

### Requirement: Source Artifact Persistence
The system SHALL download and store the raw source documents (PDFs) locally to ensure audit reproducibility and offline availability.

#### Scenario: Caching the PDF
- **WHEN** the Extractor Agent receives a valid PDF URL
- **THEN** it MUST download the file to `data/cache/artifacts/{id}_{year}.pdf`.
- **AND** all subsequent text extraction MUST be performed on this local file, not the remote URL.

#### Scenario: Broken Remote Link
- **WHEN** a re-run is triggered and the external website is down (404/500)
- **BUT** the file exists in `data/cache/artifacts/`
- **THEN** the workflow MUST proceed using the local copy without error.

### Requirement: Document Recency (Scout)
The Scout Agent SHALL prioritize the most recent available financial documentation.

#### Scenario: Multi-year document availability
- **WHEN** the website lists Annual Reports for multiple years
- **THEN** the Scout MUST select the most recent version available.

### Requirement: Statutory Data Extraction (LSG Only)
The Extractor Agent SHALL identify compliance data points defined in the LSG Manual.

#### Scenario: LSG Reserve Calculation
- **WHEN** processing an LSG-subvented NGO
- **THEN** the agent MUST extract the `lsg_reserve_amount` and `operating_expenditure`.
- **AND** calculate if the reserve exceeds 25% of operating expenditure.

### Requirement: Hallucination Defense
The system SHALL NOT infer data that is not explicitly present in the text.

#### Scenario: Ambiguous Financials
- **WHEN** the document does not explicitly state "Program Expenses"
- **THEN** the agent MUST return `null`.

### Requirement: Binary Audit Computation
The system MUST compute a series of pass/fail check-items based on extracted statutory and financial data.

#### Scenario: Reserve Cap Validation
- **GIVEN** an NGO has a cumulative LSG reserve of $1M and operating expenses of $3M
- **WHEN** the audit logic calculates the ratio (0.33)
- **THEN** the `check_reserve_cap` item MUST return `status: "fail"`
- **AND** include the calculation details in the `details` field.

