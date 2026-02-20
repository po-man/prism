# audit-workflows Specification (Delta)

## ADDED Requirements
### Requirement: Cloud-Native Artifact Caching for Intelligence Processing
The system SHALL utilize cloud-native file APIs (e.g., the Gemini File API) for processing large documents to bypass inline payload limits, and SHALL cache these remote references locally to minimize redundant network uploads, reduce latency, and respect API rate limits.

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