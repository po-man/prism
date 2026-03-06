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
The `utils_api` SHALL calculate the cost per outcome based on cumulative impact and additionally provide a normalised translation for a standard retail donation amount ($1,000).

#### Scenario: Protecting Cost Per Outcome from Temporal Leakage
- **WHEN** `check_cost_per_outcome` falls back to summing values from the `metrics` array (because `beneficiaries.population` is zero or unavailable)
- **THEN** the function MUST strictly filter the `metrics` array and only sum quantitative values where the `timeframe` attribute is exactly `"annual"`.
- **AND** it MUST ignore any metrics marked as `"cumulative"` or `"unspecified"` to preserve the integrity of the ratio against the annual financial expenditure.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, and ensuring temporal and mathematical consistency.

#### Scenario: Temporal Classification and Demographic Reconciliation
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST instruct the model to strictly classify every extracted metric and event as `annual` (occurring within the reporting year), `cumulative` (spanning multiple years or since inception), or `unspecified`.
- **AND** the system prompt MUST explicitly instruct the model to mathematically reconcile the total `population` in the `beneficiaries` array to reflect the *annual* total of animals helped, ensuring it aligns logically with the scale of the extracted annual `metrics`.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts and prioritized impact models.

#### Scenario: Extracting Pan-Asian Metadata and Sorted Impact
- **WHEN** generating prompts for the Gemini model
- **THEN** the metadata system prompt MUST instruct the model to locate any official government non-profit registration ID globally, mapping it to `registration_id`.
- **AND** the impact system prompt MUST instruct the model to extract exact verbatim sentences as `evidence_quote` to justify evidence quality.
- **AND** the impact system prompt MUST instruct the model to sort the `significant_events` and `metrics` arrays in descending order of significance or scale of impact.

### Requirement: Document Ingestion Pipeline
The n8n orchestrator SHALL ingest target charities and their source documents, gracefully combining available PDFs with targeted web intelligence to maximize data extraction.

#### Scenario: Omni-Channel Impact Data Collection
- **WHEN** the primary analysis workflow is triggered and fetches charity data
- **THEN** it MUST dynamically construct and execute a web search query (e.g., `site:example.org (impact OR rescued OR animals OR annual OR report OR metrics)`) using the charity's official domain extracted during the metadata phase.
- **AND** it MUST aggregate the top search results into a clean `<web_context>` snippet string.
- **AND** the workflow MUST route to the Impact extraction branch if either an `annual_report` PDF exists OR the `domains` array is not empty (yielding web snippets).

