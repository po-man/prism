# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions tailored to animal advocacy, weighting neglectedness by proportional population impact.

#### Scenario: Evaluating Neglectedness Proportions
- **WHEN** the `utils_api` executes `check_cause_area_neglectedness`
- **THEN** it MUST calculate the total population by summing the `population` field of all items in the `beneficiaries` array.
- **AND** if population data is available, it MUST calculate the relative percentage of high-neglectedness types (`"farmed_animals"`, `"wild_animals"`).
- **AND** if the combined high-neglectedness proportion is >= 50%, the status SHALL be `pass`.
- **AND** if the combined high-neglectedness proportion is > 0% but < 50%, the status SHALL be `warning` (Mixed Neglectedness), with the calculation string noting the specific breakdown.
- **AND** if the proportion of `"companion_animals"` is 100%, the status SHALL be `warning` (Low Neglectedness / Saturated space).
- **AND** if all `population` fields are `null`, the function MUST fall back to the legacy presence/absence logic.

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount ($1,000).

#### Scenario: Appending Retail Translation to Cost Per Outcome
- **WHEN** `check_cost_per_outcome` successfully calculates a valid positive cost per outcome
- **THEN** the function MUST calculate how many outcomes can be achieved with $1,000 (i.e., `1000 / cost_per_outcome`).
- **AND** append this translation to the `base_item.details.calculation` string (e.g., "... per outcome. | A $1,000 donation achieves ≈ X outcomes.").

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations.

#### Scenario: EA Animal Impact Extraction
- **WHEN** querying via LLM
- **THEN** the system prompt MUST instruct the model to prioritize quantitative data regarding animal lives improved/spared.
- **AND** the prompt MUST instruct the model to explicitly extract the exact `population` count for *each* `beneficiary_type` if the charity serves multiple categories of animals.
- **AND** the prompt MUST strictly instruct the model to classify evidence quality according to the ITN framework.

