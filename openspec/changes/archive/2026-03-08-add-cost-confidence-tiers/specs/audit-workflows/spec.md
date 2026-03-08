## MODIFIED Requirements

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount, dynamically assigning a Confidence Tier to prevent misrepresentation of multi-domain charities.

#### Scenario: Evaluating High Confidence Unit Costs
- **WHEN** `check_cost_per_outcome` executes AND `impact.context.explicit_unit_cost` is populated
- **THEN** it MUST convert the explicitly stated amount to USD (using the financial exchange rate).
- **AND** it MUST set the `confidence_tier` to `HIGH` and the `confidence_note` to "This unit cost is explicitly stated by the organisation in their reporting."

#### Scenario: Evaluating Medium Confidence Unit Costs
- **WHEN** `explicit_unit_cost` is null AND `operating_scope` is `pure_animal_advocacy`
- **THEN** it MUST calculate the cost by dividing total program services expenditure (USD) by total animal beneficiaries.
- **AND** it MUST set the `confidence_tier` to `MEDIUM` and the `confidence_note` to "This unit cost is estimated by PRISM by dividing total programme expenditure by the total quantified animal beneficiaries."

#### Scenario: Aborting Low Confidence Unit Costs
- **WHEN** `explicit_unit_cost` is null AND `operating_scope` is `multi_domain_operations`
- **THEN** it MUST set the metric `value` to `null`.
- **AND** it MUST set the `confidence_tier` to `LOW` and the `confidence_note` to "Cost per outcome calculation is not available. This organisation conducts significant multi-domain work (e.g., human education, environmental conservation). Dividing the total budget solely by quantified animal outcomes would artificially inflate the cost and misrepresent their financial efficiency."

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and ensuring temporal and mathematical consistency.

#### Scenario: Prompting for Operating Scope and Explicit Costs
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt MUST explicitly instruct the model to analyse the charity's overall mission and classify `operating_scope` as `multi_domain_operations` if significant funds or efforts are directed toward humans, broad environmental policy, or non-animal beneficiaries.
- **AND** it MUST instruct the model to aggressively search for and extract any explicitly stated "cost per intervention" or "cost per animal" directly into the `explicit_unit_cost` object.