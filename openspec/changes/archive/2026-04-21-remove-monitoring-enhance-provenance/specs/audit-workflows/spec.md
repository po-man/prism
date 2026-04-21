## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations and maintaining strict data provenance.

#### Scenario: Extracting Counterfactual Quotes
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST strictly instruct the model to locate the exact verbatim text justifying the `counterfactual_baseline`.
- **AND** it MUST place this exact sentence in the `source.quote` field, rather than paraphrasing or synthesising a description.

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, explicitly declaring the threshold rules for every evaluation to ensure complete auditability.

#### Scenario: Injecting Evaluation Criteria
- **WHEN** any check function within `utils_api/app/audits/impact.py` or `financials.py` instantiates an `AuditDetails` model
- **THEN** it MUST populate the `criteria` field with a concise, human-readable explanation of the Pass/Warn/Fail thresholds specific to that check.

#### Scenario: Counterfactual Baseline Elaboration
- **WHEN** executing `check_counterfactual_baseline`
- **THEN** the function MUST map the newly extracted `counterfactual_baseline.source.quote` directly into the `base_item.details.elaboration` field so it renders in the checklist UI.