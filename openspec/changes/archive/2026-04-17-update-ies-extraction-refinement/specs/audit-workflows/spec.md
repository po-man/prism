## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Enforcing Zero-Hallucination Constraints
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly enforce the following constraints to prevent data hallucinations:
  1. **Beneficiary Classification:** "Egg counts (e.g., '10,000 eggs secured') MUST be quantified and classified as individual beneficiaries and outcomes, subject to standard moral weighting."
  2. **Exclusion of Potential Impact:** "Metrics regarding 'potential' animals helped, 'capacity to hold', or 'future targets' MUST NOT be extracted as outcome counts or beneficiaries. Only historically realised, explicit physical counts are permitted."
  3. **Financial Value Disambiguation:** "Dollar amounts, funds raised, or monetary values MUST NEVER be extracted as quantitative animal counts. Differentiate strictly between a currency symbol/word and a biological organism."
  4. **Operating Scope Definition:** "Conducting humane education, managing human volunteers, or running awareness campaigns about animals DOES NOT constitute a multi-domain operation. The organisation remains `pure_animal_advocacy` unless a significant portion of its core financial budget is diverted to non-animal sectors (e.g., human humanitarian aid)."

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