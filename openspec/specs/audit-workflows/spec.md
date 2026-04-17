# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system, separating intervention-level tractability from organisation-level monitoring capabilities.

#### Scenario: Metric-to-Intervention Attribution
- **WHEN** the impact engine attempts to map a metric to a significant event to determine the Leverage Multiplier ($W_{leverage}$)
- **THEN** it MUST utilise a fuzzy matching heuristic (e.g., substring normalisation or Levenshtein distance) rather than strict exact-string matching.
- **AND** if an explicit match still fails, the engine MUST NOT drop the metric; instead, it MUST assign the metric to the charity's primary intervention or apply a conservative sector-average baseline probability.

#### Scenario: Leverage Multiplier ($W_{leverage}$) Resolution
- **WHEN** an event is tagged with multiple interventions
- **THEN** the engine MUST identify the intervention marked as `is_primary` and exclusively apply its $W_{leverage}$.
- **AND** it MUST NOT default to selecting the maximum $W_{leverage}$ from the array.

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalised translation for a standard retail donation amount, ensuring all cross-charity comparisons use a unified USD baseline and accurate mathematical scaling.

#### Scenario: Applying the Scale Multiplier Before Currency Conversion
- **WHEN** the `utils_api` retrieves financial data to compute total expenditures or `check_cost_per_outcome`
- **THEN** the engine MUST first calculate the true local value by multiplying the `value` by the `scale_multiplier`.
- **AND** this scaled local value MUST then be used for the subsequent `usd_exchange_rate` conversion and final cost-per-outcome division.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Enforcing Zero-Hallucination Constraints
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly enforce the following constraints to prevent data hallucinations:
  1. **Beneficiary Classification:** "Egg counts (e.g., '10,000 eggs secured') MUST be quantified and classified as individual beneficiaries and outcomes, subject to standard moral weighting."
  2. **Exclusion of Potential Impact:** "Metrics regarding 'potential' animals helped, 'capacity to hold', or 'future targets' MUST NOT be extracted as outcome counts or beneficiaries. Only historically realised, explicit physical counts are permitted."
  3. **Financial Value Disambiguation:** "Dollar amounts, funds raised, or monetary values MUST NEVER be extracted as quantitative animal counts. Differentiate strictly between a currency symbol/word and a biological organism."
  4. **Operating Scope Definition:** "Conducting humane education, managing human volunteers, or running awareness campaigns about animals DOES NOT constitute a multi-domain operation. The organisation remains `pure_animal_advocacy` unless a significant portion of its core financial budget is diverted to non-animal sectors (e.g., human humanitarian aid)."

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

### Requirement: LLM Prompt Injection for Financials
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate financial data while adhering to a strict "no-inference" policy.

#### Scenario: Extracting Header and Footnote Unit Scales
- **WHEN** generating prompts for the Gemini model in the Financial extraction node
- **THEN** the system prompt MUST explicitly instruct the model to scan table headers, sub-headers, and footnotes for phrasing such as "in thousands", "'000", "in millions", or "mn".
- **AND** the prompt MUST instruct the model to extract the raw number exactly as written into the `value` field, without attempting to perform mental arithmetic (e.g., adding zeroes).
- **AND** the prompt MUST instruct the model to set the `scale_multiplier` field to `1000` or `1000000` corresponding to the discovered scale, or `1` if no scale is specified.

