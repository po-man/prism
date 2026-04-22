## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations and maintaining strict data provenance.

#### Scenario: Strict Extraction of Per-Animal Unit Costs
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST instruct the model to ONLY extract an `explicit_unit_cost` if the cost is explicitly stated per individual animal or a discrete, singular outcome.
- **AND** the prompt MUST explicitly prohibit extracting aggregate budgets, total grant awards, monthly operational costs, or overall fundraising campaign goals into this array.