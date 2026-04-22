## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs and maintain strict data provenance.

#### Scenario: Enforcing Strict Nulls for Missing Evidence
- **WHEN** the LLM cannot locate explicit evidence for a requested field (such as a counterfactual quote)
- **THEN** the system prompt MUST strictly instruct the model to output a native JSON `null`.
- **AND** the model MUST be explicitly forbidden from populating string fields with denial phrases like "Not found", "None", "Unspecified", or "N/A".

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, strictly validating data to prevent false positives from LLM hallucinations.

#### Scenario: Multi-Tier Counterfactual Baseline with Heuristic Sanitisation
- **WHEN** executing `check_counterfactual_baseline`
- **THEN** the function MUST evaluate all metrics for counterfactual data.
- **AND** it MUST sanitise any provided `source.quote` by checking against a blacklist of denial phrases and ensuring a minimum character length (e.g., > 10 characters).
- **AND** if a metric contains a `counterfactual_baseline` with a `value` AND a valid sanitised `source.quote`, the status MUST be `pass`.
- **AND** if no quantified baseline exists, but a metric contains a valid sanitised `source.quote` (qualitative baseline), the status MUST be `warning`.
- **AND** if the quote fails sanitisation (e.g., "No statement found"), it MUST be treated as `null`, resulting in a `fail`.