# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system, separating intervention-level tractability from organisation-level monitoring capabilities.

#### Scenario: Aggregating an Intervention Leverage Portfolio
- **WHEN** the `check_intervention_tractability` function evaluates the `significant_events` array
- **THEN** it MUST map all interventions with verifiable source quotes to their corresponding "Intervention Leverage Tiers" (Tier 1: Systemic Change, Tier 2: Preventative Scale, Tier 3: Direct Care & Indirect Action).
- **AND** it MUST determine the highest tier achieved and inject it as a string into the `details.calculation` field.
- **AND** it MUST compile all verified interventions, grouped by tier, into a single structured list of dictionaries. This list MUST be serialized into a JSON string and injected into the `details.elaboration` field so the UI can parse and render the complete portfolio.
- **AND** it MUST assign a "pass" status if the organisation possesses at least one verified Tier 1 or Tier 2 intervention, and a "warning" if the portfolio consists solely of Tier 3 interventions or if no verifiable interventions are present.

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

#### Scenario: Instructing the LLM on Epistemic Humility
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly instruct the LLM to search for admissions of failure, unintended consequences, or negative impacts within the text.
- **AND** it MUST instruct the LLM to search for exact euthanasia or live-release numbers, explicitly warning the LLM *not* to infer these numbers from generic "animals saved" metrics.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritized impact models, and highly traceable data provenance.

#### Scenario: Line-Item Financial Provenance Instructions
- **WHEN** generating system prompts for the Gemini model to extract financial data
- **THEN** the prompt MUST instruct the model to attach a specific `source` object to *every* extracted financial figure.
- **AND** the prompt MUST explicitly prohibit summarising sources into a top-level array, forcing the LLM to justify each extracted number (e.g., `income.donations.source`) with its exact, absolute page number and verifiable verbatim quote.

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

#### Scenario: Recursive Deep-Link Injection for Financials
- **WHEN** the Orchestrator passes the `financials` payload to the `/resolve-provenance` endpoint
- **THEN** it MUST transmit the entire, nested `financials` object rather than a flat array.
- **AND** the recursive `_find_and_resolve_sources` logic MUST automatically traverse the nested `income`, `expenditure`, and `reserves` objects, mutating and injecting the `resolved_url` for every discovered line-item source.

### Requirement: Epistemic Humility Audit Logic
The `utils_api` microservice SHALL execute deterministic transparency audit functions to reward epistemic humility and operational transparency, utilising the Advanced Check taxonomy (`bonus`, `not_disclosed`, `n_a`).

#### Scenario: Evaluating Negative Impact Disclosure
- **WHEN** the `check_negative_impact_disclosure` function evaluates the `transparency_indicators`
- **THEN** it MUST assign a `bonus` status if `unintended_consequences_reported` is true and verified with a source.
- **AND** it MUST assign a `not_disclosed` status if it is false, explicitly noting that non-disclosure is the industry norm and does not constitute a failure.

#### Scenario: Conditionally Evaluating Live Release Rates
- **WHEN** the `check_live_release_transparency` function executes
- **THEN** it MUST first scan the `significant_events` array for `individual_rescue_and_sanctuary` or `veterinary_care_and_treatment`.
- **AND** if neither intervention is present, the audit MUST immediately return an `n_a` (Not Applicable) status with the calculation "Organisation does not engage in direct animal sheltering; metric not applicable."
- **AND** if applicable, it MUST evaluate `euthanasia_statistics_reported`, returning `bonus` for true, and `not_disclosed` for false.

