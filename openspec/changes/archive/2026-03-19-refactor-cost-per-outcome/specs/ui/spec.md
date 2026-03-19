## MODIFIED Requirements

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, dynamically suppressing the calculation if the data confidence is low.

#### Scenario: Rendering Arrays of Intervention-Specific Costs
- **WHEN** rendering the Value for Money component on a charity's individual profile (`myth-buster.html`)
- **THEN** the template MUST parse the `cost_per_outcome` metric to determine if multiple intervention-specific costs were identified (e.g., from the `explicit_unit_costs` array).
- **AND** if multiple costs exist, it MUST render them as a list, displaying the specific intervention name (e.g., "High Volume Spay Neuter: $25", "Individual Rescue: $450") instead of a single blended number.
- **AND** if the metric was derived via the Pure-Play cohort logic, it MUST display a specific badge or text indicating it as a "Pure-Play Benchmark".