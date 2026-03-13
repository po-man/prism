## MODIFIED Requirements

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system, separating intervention-level tractability from organisation-level monitoring capabilities.

#### Scenario: Aggregating an Intervention Leverage Portfolio
- **WHEN** the `check_intervention_tractability` function evaluates the `significant_events` array
- **THEN** it MUST map all interventions with verifiable source quotes to their corresponding "Intervention Leverage Tiers" (Tier 1: Systemic Change, Tier 2: Preventative Scale, Tier 3: Direct Care & Indirect Action).
- **AND** it MUST determine the highest tier achieved and inject it as a string into the `details.calculation` field.
- **AND** it MUST compile all verified interventions, grouped by tier, into a single structured list of dictionaries. This list MUST be serialized into a JSON string and injected into the `details.elaboration` field so the UI can parse and render the complete portfolio.
- **AND** it MUST assign a "pass" status if the organisation possesses at least one verified Tier 1 or Tier 2 intervention, and a "warning" if the portfolio consists solely of Tier 3 interventions or if no verifiable interventions are present.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Enforcing Expanded Intervention Classification
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST include a comprehensive rubric explicitly defining all 13 acceptable `intervention_type` options.
- **AND** it MUST instruct the model to accurately classify events according to their systemic leverage (e.g., mapping legislative wins to `policy_and_legal_advocacy` and street activism to `vegan_outreach_and_dietary_change`), only resorting to the `other` fallback when absolutely necessary.