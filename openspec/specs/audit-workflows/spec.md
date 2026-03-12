# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system, separating intervention-level tractability from organisation-level monitoring capabilities.

#### Scenario: Evaluating Intervention Tractability against EA Ground Truth
- **WHEN** the audit engine evaluates a charity's impact data
- **THEN** a dedicated function (`check_intervention_tractability`) MUST map the extracted `intervention_type` arrays from all `significant_events` against a static, predefined EA `INTERVENTION_TRACTABILITY_MAP`.
- **AND** it MUST assign a status based on the highest tractability tier found (e.g., `pass` for RCT/Quasi-Experimental, `warning` for lower tiers).
- **AND** the calculation details MUST output the specific intervention type matched alongside the EA rationale note from the map.

#### Scenario: Evaluating Organisation-Level M&E Capacity
- **WHEN** the audit engine evaluates the `metrics` array
- **THEN** the existing logic evaluating the charity's self-reported `evidence_quality` MUST be preserved but formally renamed and re-categorised as `check_monitoring_and_evaluation`.
- **AND** it MUST reflect the charity's internal rigour, independent of general intervention tractability.

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
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Semantic Rubric Injection for Interventions
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST include explicit, concise definitions for every allowed enum value in `intervention_type` to guide the LLM's classification logic and minimise the usage of "other".
- **AND** the prompt MUST instruct the model to provide a 3-5 word summary in `intervention_type_other_description` ONLY if "other" is selected.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritized impact models, and highly traceable data provenance.

#### Scenario: Enforcing Absolute PDF Page Indexing
- **WHEN** generating system prompts for the Gemini model to extract data from PDFs
- **THEN** the prompt MUST explicitly instruct the LLM to populate the `source` object's `page_number` field using the **1-based absolute PDF page index**.
- **AND** the prompt MUST strictly instruct the LLM to ignore any printed page numbers found in the document's headers or footers (e.g., Roman numerals, "Page 2 of 50"), as these will break browser PDF routing.
- **AND** the prompt MUST instruct the LLM to extract exact verbatim sentences into the `quote` field of the `source` object for all data points.

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

### Requirement: Centralised Provenance Resolution Endpoint
The `utils_api` microservice SHALL provide a dedicated endpoint (e.g., `/resolve-provenance`) to programmatically convert raw LLM citations into exact, browser-routable deep links.

#### Scenario: Resolving PDF Deep Links
- **WHEN** the `utils_api` receives a payload containing a `source` object where `source_type` is `annual_report` or `financial_report`
- **THEN** it MUST read the corresponding base URL provided in the request context.
- **AND** it MUST append `#page=N` to the URL (where N is the `page_number` integer).
- **AND** it MUST assign this concatenated string to the `resolved_url` field.

#### Scenario: Resolving Web Text Fragments
- **WHEN** the `utils_api` receives a payload containing a `source` object where `source_type` is `web_search`
- **THEN** it MUST locate the correct URL and original snippet from the provided `web_search_results` context array using the `search_result_index`.
- **AND** it MUST generate a W3C Text Fragment (`#:~:text=...`) using the `quote` string.
- **AND** it MUST assign the combined URL and fragment to the `resolved_url` field.

