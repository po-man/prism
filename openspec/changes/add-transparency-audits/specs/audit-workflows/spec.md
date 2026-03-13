## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Instructing the LLM on Epistemic Humility
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly instruct the LLM to search for admissions of failure, unintended consequences, or negative impacts within the text.
- **AND** it MUST instruct the LLM to search for exact euthanasia or live-release numbers, explicitly warning the LLM *not* to infer these numbers from generic "animals saved" metrics.