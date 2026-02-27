## ADDED Requirements

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount ($1,000).

#### Scenario: Appending Retail Translation to Cost Per Outcome
- **WHEN** `check_cost_per_outcome` successfully calculates a valid positive cost per outcome
- **THEN** the function MUST calculate how many outcomes can be achieved with $1,000 (i.e., `1000 / cost_per_outcome`).
- **AND** append this translation to the `base_item.details.calculation` string (e.g., "... per outcome. | A $1,000 donation achieves ≈ X outcomes.").