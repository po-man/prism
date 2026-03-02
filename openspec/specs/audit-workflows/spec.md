# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system.

#### Scenario: Executing Three-Tier Thresholds
- **WHEN** the `utils_api` evaluates quantitative data
- **THEN** it MUST apply the following boundaries:
  - `check_liquidity`: `pass` (>= 6 months), `warning` (>= 3 and < 6 months), `fail` (< 3 months).
  - `check_reserve_cap`: `pass` (<= 2 years), `warning` (> 2 and <= 5 years), `fail` (> 5 years).
  - `check_funding_neglectedness`: `pass` (< 40% government grants), `warning` (>= 40% and <= 80%), `fail` (> 80%).
  - `check_cause_area_neglectedness`: `pass` (>= 50% high-neglectedness), `warning` (> 0% and < 50%), `fail` (0% high-neglectedness).

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount ($1,000), persisting it outside the boolean check array.

#### Scenario: Generating Calculated Metrics
- **WHEN** the `utils_api` processes the audit payload
- **THEN** it MUST execute the `cost_per_outcome` calculation and append it to the new `calculated_metrics` array, entirely independent of the `check_items` array.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations.

#### Scenario: EA Animal Impact Extraction
- **WHEN** querying via LLM
- **THEN** the system prompt MUST instruct the model to prioritize quantitative data regarding animal lives improved/spared.
- **AND** the prompt MUST instruct the model to explicitly extract the exact `population` count for *each* `beneficiary_type` if the charity serves multiple categories of animals.
- **AND** the prompt MUST strictly instruct the model to classify evidence quality according to the ITN framework.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts and prioritized impact models.

#### Scenario: Extracting Pan-Asian Metadata and Sorted Impact
- **WHEN** generating prompts for the Gemini model
- **THEN** the metadata system prompt MUST instruct the model to locate any official government non-profit registration ID globally, mapping it to `registration_id`.
- **AND** the impact system prompt MUST instruct the model to extract exact verbatim sentences as `evidence_quote` to justify evidence quality.
- **AND** the impact system prompt MUST instruct the model to sort the `significant_events` and `metrics` arrays in descending order of significance or scale of impact.

