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

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount ($1,000).

#### Scenario: Appending Retail Translation to Cost Per Outcome
- **WHEN** `check_cost_per_outcome` successfully calculates a valid positive cost per outcome
- **THEN** the function MUST calculate how many outcomes can be achieved with $1,000 (i.e., `1000 / cost_per_outcome`).
- **AND** append this translation to the `base_item.details.calculation` string (e.g., "... per outcome. | A $1,000 donation achieves ≈ X outcomes.").

