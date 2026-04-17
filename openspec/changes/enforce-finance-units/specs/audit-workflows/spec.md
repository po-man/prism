## ADDED Requirements

### Requirement: LLM Prompt Injection for Financials
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate financial data while adhering to a strict "no-inference" policy.

#### Scenario: Extracting Header and Footnote Unit Scales
- **WHEN** generating prompts for the Gemini model in the Financial extraction node
- **THEN** the system prompt MUST explicitly instruct the model to scan table headers, sub-headers, and footnotes for phrasing such as "in thousands", "'000", "in millions", or "mn".
- **AND** the prompt MUST instruct the model to extract the raw number exactly as written into the `value` field, without attempting to perform mental arithmetic (e.g., adding zeroes).
- **AND** the prompt MUST instruct the model to set the `scale_multiplier` field to `1000` or `1000000` corresponding to the discovered scale, or `1` if no scale is specified.

## MODIFIED Requirements

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalised translation for a standard retail donation amount, ensuring all cross-charity comparisons use a unified USD baseline and accurate mathematical scaling.

#### Scenario: Applying the Scale Multiplier Before Currency Conversion
- **WHEN** the `utils_api` retrieves financial data to compute total expenditures or `check_cost_per_outcome`
- **THEN** the engine MUST first calculate the true local value by multiplying the `value` by the `scale_multiplier`.
- **AND** this scaled local value MUST then be used for the subsequent `usd_exchange_rate` conversion and final cost-per-outcome division.