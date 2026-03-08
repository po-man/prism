## MODIFIED Requirements

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

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Semantic Rubric Injection for Interventions
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST include explicit, concise definitions for every allowed enum value in `intervention_type` to guide the LLM's classification logic and minimise the usage of "other".
- **AND** the prompt MUST instruct the model to provide a 3-5 word summary in `intervention_type_other_description` ONLY if "other" is selected.