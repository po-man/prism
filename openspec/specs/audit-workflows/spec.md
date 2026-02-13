# audit-workflows Specification

## Purpose
TBD - created by archiving change add-audit-workflows. Update Purpose after archive.
## Requirements
### Requirement: Idempotent Execution & State Persistence
The system SHALL employ a checkpointing strategy to ensure that high-cost operations are not repeated unnecessarily.

#### Scenario: Cache Hit (Skip Execution)
- **WHEN** a sub-workflow is triggered
- **AND** a valid cache file exists
- **THEN** the system MUST read and return the data from the file.

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

