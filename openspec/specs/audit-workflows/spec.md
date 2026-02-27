# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions tailored to animal advocacy.

#### Scenario: Evaluating Neglectedness
- **WHEN** the `utils_api` processes the `impact` data object
- **THEN** it MUST execute a `check_cause_area_neglectedness` function.
- **AND** if the `beneficiary_type` is `"farmed_animals"` or `"wild_animals"`, the status SHALL be `pass` (High Neglectedness).
- **AND** if the `beneficiary_type` is `"companion_animals"`, the status SHALL be `warning` (Low Neglectedness / Saturated space), reflecting EA resource allocation principles.

