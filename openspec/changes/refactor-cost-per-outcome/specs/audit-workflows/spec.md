## MODIFIED Requirements

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount, dynamically assigning a Confidence Tier to prevent misrepresentation of multi-domain charities.

#### Scenario: Evaluating High Confidence Unit Costs from Arrays
- **WHEN** `check_cost_per_outcome` executes AND the `explicit_unit_costs` array contains one or more valid entries
- **THEN** the audit function MUST evaluate and convert each explicitly stated amount to USD.
- **AND** it MUST set the `confidence_tier` to `HIGH` and output a structured list of these costs, explicitly noting the intervention type they apply to.

#### Scenario: Medium Confidence via Programmatic Financial Matching
- **WHEN** `explicit_unit_costs` is empty AND `program_breakdowns` contains valid financial data
- **THEN** the system MUST attempt to match the `programme_name` to a reported intervention in `significant_events` or a specific beneficiary group.
- **AND** if a reasonable match is found, it MUST divide that specific programmatic spend by the specific outcome population to calculate an intervention-specific cost.
- **AND** it MUST set the `confidence_tier` to `MEDIUM` with a note explaining the programmatic derivation.

#### Scenario: Medium Confidence via Pure-Play Cohorts
- **WHEN** granular programmatic matching is not possible
- **THEN** the system MUST evaluate if the charity is a "Pure-Play" organisation (defined as allocating >80% of its `program_services` expenditure to a single, identifiable intervention type).
- **AND** if it qualifies as a Pure-Play, the system MUST divide total programmatic spend by the primary outcome, labelling the result as a benchmarkable Pure-Play cost with `MEDIUM` confidence.

#### Scenario: Aborting Low Confidence Unit Costs for Unattributable Multi-Domain Charities
- **WHEN** the charity is multi-domain, lacks explicit unit costs, is not a Pure-Play, and lacks attributable programmatic financial breakdowns
- **THEN** the system MUST set the metric `value` to `null`.
- **AND** it MUST set the `confidence_tier` to `LOW`, explaining that dividing a multi-domain budget by a lumped sum of outcomes would produce a mathematically distorted and misleading cost.