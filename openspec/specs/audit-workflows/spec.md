# audit-workflows Specification

## Purpose
This specification defines the system's core data processing pipelines, managed by the n8n orchestrator. It covers the entire workflow from data ingestion and parallel extraction (document parsing and web search) to the final evaluation by the "Audit Checklist Engine." This includes the logic for calling external services (like Gemini for AI extraction and PocketBase for persistence) and the deterministic rules for generating the standardised `check_items` array based on financial, impact, and risk criteria.
## Requirements
### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, strictly validating data to prevent false positives from LLM hallucinations.

#### Scenario: Multi-Tier Counterfactual Baseline with Heuristic Sanitisation
- **WHEN** executing `check_counterfactual_baseline`
- **THEN** the function MUST evaluate all metrics for counterfactual data.
- **AND** it MUST sanitise any provided `source.quote` by checking against a blacklist of denial phrases and ensuring a minimum character length (e.g., > 10 characters).
- **AND** if a metric contains a `counterfactual_baseline` with a `value` AND a valid sanitised `source.quote`, the status MUST be `pass`.
- **AND** if no quantified baseline exists, but a metric contains a valid sanitised `source.quote` (qualitative baseline), the status MUST be `warning`.
- **AND** if the quote fails sanitisation (e.g., "No statement found"), it MUST be treated as `null`, resulting in a `fail`.

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalised translation for a standard retail donation amount, ensuring all cross-charity comparisons use a unified USD baseline and accurate mathematical scaling.

#### Scenario: Applying the Scale Multiplier Before Currency Conversion
- **WHEN** the `utils_api` retrieves financial data to compute total expenditures or `check_cost_per_outcome`
- **THEN** the engine MUST first calculate the true local value by multiplying the `value` by the `scale_multiplier`.
- **AND** this scaled local value MUST then be used for the subsequent `usd_exchange_rate` conversion and final cost-per-outcome division.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations and forcing the model to explicitly assign reference keys from the database.

#### Scenario: Dynamic Reference Enum Injection
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the orchestrator MUST dynamically fetch the live `species_key` and `intervention_key` lists from the Data Vault.
- **AND** it MUST inject these live lists into the JSON schema as strict enum constraints.
- **AND** the system prompt MUST instruct the model to evaluate the qualitative context of the metric and select the single most appropriate `species_key` and `intervention_key` from the provided enums.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritised impact models, and highly traceable data provenance.

#### Scenario: Injecting Lightweight Schemas in n8n
- **WHEN** the "Prepare Prompts" sub-workflow executes the "Read JSON schema" nodes
- **THEN** it MUST target the newly generated extraction schemas (e.g., `impact.extract.schema.json`) located in the mounted schemas directory.
- **AND** the subsequent Gemini extraction nodes MUST use these lightweight schemas to guide the FSM, whilst relying on the modified `description` fields to enforce semantic classification and enum adherence.

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

#### Scenario: Resolving PDF Provenance
- **WHEN** the Orchestrator passes the payload to the `/resolve-provenance` endpoint
- **THEN** the recursive `_find_and_resolve_sources` logic MUST ONLY process sources where `source_type` is `attached_report`.
- **AND** it MUST construct the `resolved_url` using the base document URL and the `#page=[page_number]` fragment.
- **AND** it MUST NOT attempt to resolve or append text fragments for web search URLs.

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
The orchestration pipeline SHALL execute a rigid, multi-stage data lineage to compute the IES, ensuring every component of the calculation retains its traceability to source documents and relies on explicitly assigned classifications rather than inferred string matching.

#### Scenario: Deterministic Reference Key Lookups
- **WHEN** the `utils_api` computes the `w_species`, `w_leverage`, and `d_evidence` for an IES metric
- **THEN** it MUST directly query the reference dictionaries using the `metric.species_key`, `metric.intervention_key`, and `metric.evidence_quality` extracted deterministically by the LLM.
- **AND** the pipeline MUST immediately bypass any fuzzy matching heuristics or substring overlap logic.
- **AND** if an exact match is not found in the reference tables, it MUST fall back to a predefined conservative baseline without attempting to infer context.

### Requirement: LLM Prompt Injection for Financials
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate financial data while adhering to a strict "no-inference" policy.

#### Scenario: Extracting Header and Footnote Unit Scales
- **WHEN** generating prompts for the Gemini model in the Financial extraction node
- **THEN** the system prompt MUST explicitly instruct the model to scan table headers, sub-headers, and footnotes for phrasing such as "in thousands", "'000", "in millions", or "mn".
- **AND** the prompt MUST instruct the model to extract the raw number exactly as written into the `value` field, without attempting to perform mental arithmetic (e.g., adding zeroes).
- **AND** the prompt MUST instruct the model to set the `scale_multiplier` field to `1000` or `1000000` corresponding to the discovered scale, or `1` if no scale is specified.

### Requirement: Document Ingestion Pipeline
The n8n orchestrator SHALL ingest target charities and their source documents, gracefully combining available PDFs with targeted web intelligence to maximize data extraction.

#### Scenario: Serialised Contextual Extraction for Impact Data
- **WHEN** the orchestrator triggers the Impact extraction phase
- **THEN** it MUST execute the extraction sub-domains sequentially in the following order: Beneficiaries $\rightarrow$ Interventions $\rightarrow$ Metrics $\rightarrow$ Transparency.
- **AND** for each subsequent step, the orchestrator MUST append the user prompts and the LLM's generated responses from all preceding steps into the `contents` array of the Gemini API payload, constructing a valid multi-turn chat history.
- **AND** this chat history MUST utilise the correct `"role": "user"` and `"role": "model"` structure to preserve the LLM's thought signature and ensure logical consistency across the charity's entire logic model.
- **AND** the workflow MUST consolidate the sequentially extracted JSON objects into a unified `impact.data` payload before persisting to the data vault.

