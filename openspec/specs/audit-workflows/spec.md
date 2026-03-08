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
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount, dynamically assigning a Confidence Tier to prevent misrepresentation of multi-domain charities.

#### Scenario: Evaluating High Confidence Unit Costs
- **WHEN** `check_cost_per_outcome` executes AND `impact.context.explicit_unit_cost` is populated
- **THEN** it MUST convert the explicitly stated amount to USD (using the financial exchange rate).
- **AND** it MUST set the `confidence_tier` to `HIGH` and the `confidence_note` to "This unit cost is explicitly stated by the organisation in their reporting."

#### Scenario: Evaluating Medium Confidence Unit Costs
- **WHEN** `explicit_unit_cost` is null AND `operating_scope` is `pure_animal_advocacy`
- **THEN** it MUST calculate the cost by dividing total program services expenditure (USD) by total animal beneficiaries.
- **AND** it MUST set the `confidence_tier` to `MEDIUM` and the `confidence_note` to "This unit cost is estimated by PRISM by dividing total programme expenditure by the total quantified animal beneficiaries."

#### Scenario: Aborting Low Confidence Unit Costs
- **WHEN** `explicit_unit_cost` is null AND `operating_scope` is `multi_domain_operations`
- **THEN** it MUST set the metric `value` to `null`.
- **AND** it MUST set the `confidence_tier` to `LOW` and the `confidence_note` to "Cost per outcome calculation is not available. This organisation conducts significant multi-domain work (e.g., human education, environmental conservation). Dividing the total budget solely by quantified animal outcomes would artificially inflate the cost and misrepresent their financial efficiency."

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and ensuring temporal and mathematical consistency.

#### Scenario: Prompting for Operating Scope and Explicit Costs
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly instruct the model to analyse the charity's overall mission and classify `operating_scope` as `multi_domain_operations` if significant funds or efforts are directed toward humans, broad environmental policy, or non-animal beneficiaries.
- **AND** it MUST instruct the model to aggressively search for and extract any explicitly stated "cost per intervention" or "cost per animal" directly into the `explicit_unit_cost` object.

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

### Requirement: Orchestrator Exchange Rate Resolution
The n8n orchestrator SHALL dynamically resolve historical exchange rates to standardise financial data without modifying the raw extracted integers.

#### Scenario: Fetching Historical Year-End Rates
- **WHEN** the LLM successfully extracts the `financials` JSON payload
- **THEN** n8n MUST parse the `financial_year` string to isolate the primary reporting year (e.g., converting "2023-24" or "2023/2024" to "2023").
- **AND** n8n MUST execute an HTTP GET request to the Frankfurter API targeting December 31st of that parsed year (e.g., `https://api.frankfurter.dev/v1/2023-12-31?base=[original_code]&symbols=USD`).
- **AND** n8n MUST map the returned rate into the `financials.currency.usd_exchange_rate` field before passing the payload to the Data Vault and Utils API.
- **AND** if the `original_code` is already "USD", n8n MUST gracefully bypass the API call and set the rate to `1.0`.

