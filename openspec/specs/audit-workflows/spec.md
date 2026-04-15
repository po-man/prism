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

#### Scenario: Evaluating High Confidence Unit Costs from Arrays
- **WHEN** `check_cost_per_outcome` executes AND the `explicit_unit_costs` array contains one or more valid entries
- **THEN** the audit function MUST evaluate and convert each explicitly stated amount to USD.
- **AND** it MUST set the `confidence_tier` to `HIGH` and output a structured list of these costs, explicitly noting the intervention type they apply to.

#### Scenario: Medium Confidence via Programmatic Financial Matching
- **WHEN** `explicit_unit_costs` is empty AND `program_breakdowns` contains valid financial data
- **THEN** the system MUST attempt to match the `programme_name` to a reported intervention in `significant_events` or a specific beneficiary group.
- **AND** if a reasonable match is found, it MUST divide that specific programmatic spend by the specific outcome population to calculate an intervention-specific cost.
- **AND** it MUST set the `confidence_tier` to `MEDIUM` with a note explaining the programmatic derivation.

#### Scenario: Medium Confidence via Pure-Play Cohorts
- **WHEN** granular programmatic matching is not possible
- **THEN** the system MUST evaluate if the charity is a "Pure-Play" organisation (defined as allocating >80% of its `program_services` expenditure to a single, identifiable intervention type).
- **AND** if it qualifies as a Pure-Play, the system MUST divide total programmatic spend by the primary outcome, labelling the result as a benchmarkable Pure-Play cost with `MEDIUM` confidence.

#### Scenario: Aborting Low Confidence Unit Costs for Unattributable Multi-Domain Charities
- **WHEN** the charity is multi-domain, lacks explicit unit costs, is not a Pure-Play, and lacks attributable programmatic financial breakdowns
- **THEN** the system MUST set the metric `value` to `null`.
- **AND** it MUST set the `confidence_tier` to `LOW`, explaining that dividing a multi-domain budget by a lumped sum of outcomes would produce a mathematically distorted and misleading cost.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Instructing the LLM on Epistemic Humility
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly instruct the LLM to search for admissions of failure, unintended consequences, or negative impacts within the text.
- **AND** it MUST instruct the LLM to search for exact euthanasia or live-release numbers, explicitly warning the LLM *not* to infer these numbers from generic "animals saved" metrics.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritised impact models, and highly traceable data provenance.

#### Scenario: Injecting Lightweight Schemas in n8n
- **WHEN** the "Prepare Prompts" sub-workflow executes the "Read JSON schema" nodes
- **THEN** it MUST target the newly generated extraction schemas (e.g., `impact.extract.schema.json`) located in the mounted schemas directory.
- **AND** the subsequent Gemini extraction nodes MUST use these lightweight schemas to guide the FSM, whilst relying on the modified `description` fields to enforce semantic classification and enum adherence.

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
- **AND** it MUST dynamically inject the verbatim `source.quote` into the `details.elaboration` string to ensure the specific admission of failure is surfaced directly to the report user.
- **AND** it MUST assign a `not_disclosed` status if it is false, explicitly noting that non-disclosure is the industry norm and does not constitute a failure.

#### Scenario: Conditionally Evaluating Live Release Rates
- **WHEN** the `check_live_release_transparency` function executes
- **THEN** it MUST first scan the `significant_events` array for `individual_rescue_and_sanctuary` or `veterinary_care_and_treatment`.
- **AND** if neither intervention is present, the audit MUST immediately return an `n_a` (Not Applicable) status with the calculation "Organisation does not engage in direct animal sheltering; metric not applicable."
- **AND** if applicable, it MUST evaluate `euthanasia_statistics_reported`, returning `bonus` for true, and `not_disclosed` for false.
- **AND** if a `bonus` is awarded, it MUST dynamically append the verbatim `source.quote` to the `details.elaboration` string.

### Requirement: Extraction Payload Reversal and Validation
The `utils_api` microservice SHALL intercept LLM extraction payloads and deterministically reverse any structural abbreviations applied during the extraction schema compilation phase before executing standard validation.

#### Scenario: Reversing Shortened Keys in `utils_api`
- **WHEN** the `utils_api` receives an unvalidated JSON payload from the orchestrator's extraction nodes
- **THEN** it MUST execute a recursive reversal function utilising the `key_mapping.json` artifact (or by dynamically reading `x-extract-key` definitions from the in-memory validation schema).
- **AND** it MUST safely swap all abbreviated keys (e.g., `other_desc`) back to their canonical long-form names (e.g., `intervention_type_other_description`).
- **AND** only after this structural restoration is complete SHALL the payload be passed to the `jsonschema.validate()` method against the canonical validation schema.

### Requirement: Impact Equivalency Score (IES) Processing Flow
The orchestration pipeline SHALL execute a rigid, multi-stage data lineage to compute the IES using the formula $IES_i = Outcomes_i \times W_{species} \times W_{leverage} \times D_{evidence}$.

#### Scenario: Executing the IES Data Lineage
- **WHEN** the n8n orchestrator passes the extracted impact payload to the `utils_api`
- **THEN** the `utils_api` MUST query PocketBase for the corresponding $W_{species}$ and $D_{evidence}$ multipliers.
- **AND** the `utils_api` MUST query PocketBase for the programmatic BOTEC probability multiplier ($W_{leverage}$).
- **AND** the `utils_api` MUST compute the final IES integer using the explicitly extracted $Outcomes_i$ claims and append the detailed mathematical breakdown to the `calculated_metrics` array before persistence.

