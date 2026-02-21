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
The Extractor Agent SHALL identify compliance data points defined in the LSG Manual using multimodal document intelligence.

#### Scenario: LSG Reserve Calculation
- **WHEN** processing an LSG-subvented NGO's PDF report
- **THEN** the agent MUST use a multimodal LLM to ingest the raw PDF, parse the complex financial tables natively, and extract the `lsg_reserve_amount` and `operating_expenditure`.
- **AND** calculate if the reserve exceeds 25% of operating expenditure.

### Requirement: Hallucination Defense
The system SHALL NOT infer data that is not explicitly present in the text or verified through search grounding.

#### Scenario: Ambiguous Financials
- **WHEN** the document does not explicitly state "Program Expenses"
- **THEN** the agent MUST return `null`.

#### Scenario: Enforcing Output Structure
- **WHEN** generating data to be passed to the validation service
- **THEN** the system MUST use native API JSON schema enforcement rather than prompt-based coercion to eliminate structural hallucinations.

### Requirement: Binary Audit Computation
The system MUST compute a series of pass/fail check-items based on extracted statutory and financial data. The system MUST employ fallback calculations if aggregate metrics are missing but component metrics are present.

#### Scenario: Reserve Cap Validation
- **GIVEN** an NGO has a cumulative LSG reserve of $1M and operating expenses of $3M
- **WHEN** the audit logic calculates the ratio (0.33)
- **THEN** the `check_reserve_cap` item MUST return `status: "fail"`
- **AND** include the calculation details in the `details` field.

#### Scenario: Liquidity Fallback Calculation
- **GIVEN** the extracted data lacks `net_current_assets`
- **BUT** the data contains `current_assets` of $5M and `current_liabilities` of $2M
- **WHEN** the audit logic evaluates liquidity
- **THEN** the system MUST dynamically calculate `net_current_assets` as $3M and proceed with the standard liquidity ratio computation.

### Requirement: Grounded Risk Assessment
The Risk Agent SHALL evaluate the reputational and regulatory risks of charities by executing real-time web searches to gather external context.

#### Scenario: Identifying Recent Scandals
- **WHEN** assessing an NGO's risk profile
- **THEN** the system MUST leverage search-grounded AI to query the live web for recent controversies, scandals, or Audit Commission reports.
- **AND** if no negative news is found, explicitly state "None" in the summaries and set flags to false.

### Requirement: Cloud-Native Artifact Caching for Intelligence Processing
The system SHALL utilize cloud-native file APIs (e.g., the Gemini File API) for processing large documents to bypass inline payload limits, and SHALL cache these remote references locally to minimize redundant network uploads, reduce latency, and respect API rate limits.

#### Scenario: Processing a large document for the first time
- **GIVEN** a source artifact for a PDF larger than 50MB exists in the local datastore
- **AND** it has no `gemini_file_uri`
- **WHEN** the main workflow triggers an extraction task for this artifact
- **THEN** the system MUST upload the file to the Gemini File API
- **AND** persist the returned `gemini_file_uri` and the current timestamp to the `source_artifacts` record for future use.

### Requirement: Modular URI Resolution
The logic for checking cloud URI expiration and re-uploading documents SHALL be isolated in a dedicated sub-workflow to maintain the idempotency and readability of the main orchestrator.

#### Scenario: Reusing an unexpired cloud document
- **GIVEN** a source artifact has previously been uploaded to the Gemini File API
- **AND** the `gemini_file_uploaded_at` timestamp is less than 46 hours old
- **WHEN** the main workflow requests a URI for extraction
- **THEN** the `Ensure Gemini URI` sub-workflow MUST return the existing `gemini_file_uri` without re-uploading the binary file.

#### Scenario: Refreshing an expired cloud document
- **GIVEN** a source artifact has a `gemini_file_uri` but the `gemini_file_uploaded_at` timestamp is older than 46 hours
- **WHEN** the main workflow requests a URI for extraction
- **THEN** the `Ensure Gemini URI` sub-workflow MUST download the binary from the local datastore, re-upload it to the Gemini File API
- **AND** update the `source_artifacts` record with the new `gemini_file_uri` and current timestamp before returning the URI.

