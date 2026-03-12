## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Preventing Extraction of Products and Potential Impacts
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly instruct the LLM to only extract *actual, historical outcomes* that occurred during the reporting period, strictly excluding any projected, guessed, or potential future beneficiaries.
- **AND** the prompt MUST explicitly prohibit the classification of animal products (e.g., eggs, meals, pounds of meat) as animal beneficiaries.

#### Scenario: Clarifying Contextual Species Classification
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST provide clear rules for assigning `beneficiary_type`. 
- **AND** it MUST explicitly state that dogs and cats fall under `companion_animals` even if they are strays or unowned community animals.
- **AND** it MUST instruct the model to use context for dual-purpose animals (e.g., pet pigs as `companion_animals` vs. agricultural pigs as `farmed_animals`).
- **AND** it MUST instruct the model to fall back to `unspecified` only when the species or context is entirely ambiguous.

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system, separating intervention-level tractability from organisation-level monitoring capabilities.

#### Scenario: Safely Parsing Unspecified Populations for Neglectedness
- **WHEN** the `check_cause_area_neglectedness` function evaluates the `beneficiaries` array
- **THEN** it MUST initialise and parse the `unspecified` population count alongside the original three types.
- **AND** the `unspecified` population MUST be included in the `total_population` denominator, naturally diluting the high-neglectedness ratio if a charity fails to specify its beneficiaries, without crashing the audit engine.