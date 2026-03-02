# openspec/changes/refactor-audit-checklist/specs/audit-workflows/spec.md

## MODIFIED Requirements

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system.

#### Scenario: Executing Three-Tier Thresholds
- **WHEN** the `utils_api` evaluates quantitative data
- **THEN** it MUST apply the following boundaries:
  - `check_liquidity`: `pass` (>= 6 months), `warning` (>= 3 and < 6 months), `fail` (< 3 months).
  - `check_reserve_cap`: `pass` (<= 2 years), `warning` (> 2 and <= 5 years), `fail` (> 5 years).
  - `check_funding_neglectedness`: `pass` (< 40% government grants), `warning` (>= 40% and <= 80%), `fail` (> 80%).
  - `check_cause_area_neglectedness`: `pass` (>= 50% high-neglectedness), `warning` (> 0% and < 50%), `fail` (0% high-neglectedness).

### Requirement: Cost Per Outcome Audit Calculation
The `utils_api` SHALL calculate the cost per outcome and additionally provide a normalized translation for a standard retail donation amount ($1,000), persisting it outside the boolean check array.

#### Scenario: Generating Calculated Metrics
- **WHEN** the `utils_api` processes the audit payload
- **THEN** it MUST execute the `cost_per_outcome` calculation and append it to the new `calculated_metrics` array, entirely independent of the `check_items` array.