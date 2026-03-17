## MODIFIED Requirements

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount, dynamically assigning a Confidence Tier to prevent misrepresentation of multi-domain charities.

#### Scenario: Calculating Unit Cost Using Granular Financial Data
- **WHEN** `calculate_cost_per_outcome` executes AND the organisation's financials contain a `granular_program_services` array with a valid cost for a specific `intervention_category`
- **THEN** the logic MUST attempt to match this category against the `metrics` array in the impact data.
- **AND** if a matching metric exists with quantified beneficiaries, it MUST calculate the unit cost specific to that intervention.
- **AND** it MUST output a `CalculatedMetric` with the composite ID `cost_per_outcome:[intervention_category]`, setting the `confidence_tier` to `HIGH` or `MEDIUM` (depending on the precision of the match), explicitly citing the granular financial line-item in the `confidence_note`.

#### Scenario: Calculating Unit Cost for Highly Specialised Charities
- **WHEN** `calculate_cost_per_outcome` executes AND granular financials are NOT available, BUT >90% of the organisation's quantified beneficiaries fall under a single `intervention_category`
- **THEN** the logic MUST allocate the entire `program_services` expenditure to that dominant intervention.
- **AND** it MUST output a `CalculatedMetric` for that specific intervention, setting the `confidence_tier` to `MEDIUM` and noting that the cost is a proxy based on the organisation's high degree of specialisation.

#### Scenario: Aborting Unit Cost Calculation for Blended Interventions
- **WHEN** `calculate_cost_per_outcome` executes AND granular financials are NOT available AND the organisation performs multiple distinct interventions at scale (no single intervention exceeds 90% of beneficiaries)
- **THEN** the logic MUST strictly ABORT the unit cost calculation for those interventions.
- **AND** it MUST output a single `CalculatedMetric` with ID `cost_per_outcome` set to `null`, `confidence_tier` set to `LOW`, and a `confidence_note` explaining that blending costs across distinct major interventions (e.g., sanctuary care and mass vaccination) produces a mathematically misleading metric.

### Requirement: LLM Prompt Injection for Impact
The system SHALL utilise prompt templates injected with JSON schemas to ensure deterministic LLM outputs, capturing accurate demographic populations, maintaining strict data provenance, identifying organizational operating scope, and classifying events using strict semantic definitions.

#### Scenario: Enforcing Intervention Taxonomy Mapping
- **WHEN** generating prompts for the Gemini model in the Impact extraction node
- **THEN** the system prompt (`impact.system.md`) MUST explicitly instruct the LLM to evaluate every extracted quantitative metric and classify it using the injected `intervention_category` enum.
- **AND** it MUST instruct the LLM to use `other` if the metric fundamentally cannot be mapped to the EA taxonomy, ensuring no forced or hallucinatory classifications occur.

### Requirement: LLM Prompt Injection for Impact and Metadata
The system SHALL utilize prompt templates injected with JSON schemas to ensure deterministic LLM outputs for pan-Asian contexts, prioritized impact models, and highly traceable data provenance.

#### Scenario: Extracting Granular Financial Line-Items
- **WHEN** generating system prompts for the Gemini model to extract financial data
- **THEN** the system prompt (`financials.system.md`) MUST explicitly instruct the model to scan the financial notes and schedules for line-item breakdowns of programme expenses.
- **AND** it MUST instruct the LLM to map these line-items into the `granular_program_services` array using the strict `intervention_category` enum, while strictly preserving the overarching `program_services` total.