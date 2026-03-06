## MODIFIED Requirements

### Requirement: Document Ingestion Pipeline
The n8n orchestrator SHALL ingest target charities and their source documents, gracefully combining available PDFs with targeted web intelligence, and queuing them for human review.

#### Scenario: Forcing Re-Verification on Update
- **WHEN** the primary analysis workflow executes the final `PATCH` request to update the organisation's `analytics`, `impact`, or `financials`
- **THEN** the payload MUST include `"publish_status": "draft"`.
- **AND** this ensures that even previously approved charities are securely hidden from the live site while their newly extracted data awaits human verification.