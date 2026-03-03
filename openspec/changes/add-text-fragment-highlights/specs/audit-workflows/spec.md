## MODIFIED Requirements

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations and maintaining strict data provenance.

#### Scenario: EA Animal Impact Extraction
- **WHEN** querying via LLM
- **THEN** the system prompt MUST instruct the model to prioritize quantitative data regarding animal lives improved/spared.
- **AND** the prompt MUST instruct the model to explicitly extract the exact `population` count for *each* `beneficiary_type` if the charity serves multiple categories of animals.
- **AND** the prompt MUST strictly instruct the model to classify evidence quality according to the ITN framework.

#### Scenario: Reconciling PDF and Web Contexts for Verifiability
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the user prompt MUST distinctly separate the PDF text context and the injected `<web_context>`.
- **AND** the system prompt MUST instruct the model to prioritize data found in formal reports over web marketing copy if discrepancies exist.
- **AND** the system prompt MUST instruct the model that if a metric or event is extracted, it MUST populate the corresponding `source_url` field with the URL provided in the snippet.
- **AND** the system prompt MUST explicitly instruct the model to extract the exact, verbatim sentence from the text into the `source_quote` field (for significant events) and the `evidence_quote` field (for metrics).