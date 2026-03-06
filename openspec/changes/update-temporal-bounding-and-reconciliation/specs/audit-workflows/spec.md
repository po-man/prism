## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, and ensuring temporal and mathematical consistency.

#### Scenario: Temporal Classification and Demographic Reconciliation
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST instruct the model to strictly classify every extracted metric and event as `annual` (occurring within the reporting year), `cumulative` (spanning multiple years or since inception), or `unspecified`.
- **AND** the system prompt MUST explicitly instruct the model to mathematically reconcile the total `population` in the `beneficiaries` array to reflect the *annual* total of animals helped, ensuring it aligns logically with the scale of the extracted annual `metrics`.

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome based on cumulative impact and additionally provide a normalised translation for a standard retail donation amount ($1,000).

#### Scenario: Protecting Cost Per Outcome from Temporal Leakage
- **WHEN** `check_cost_per_outcome` falls back to summing values from the `metrics` array (because `beneficiaries.population` is zero or unavailable)
- **THEN** the function MUST strictly filter the `metrics` array and only sum quantitative values where the `timeframe` attribute is exactly `"annual"`.
- **AND** it MUST ignore any metrics marked as `"cumulative"` or `"unspecified"` to preserve the integrity of the ratio against the annual financial expenditure.