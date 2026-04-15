## ADDED Requirements

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score ($IES$) in a dedicated, self-explanatory component on the individual charity profile, breaking down the deterministic variables used in the calculation.

#### Scenario: Visualising the IES Formula
- **WHEN** rendering a charity's profile page
- **THEN** the Hugo template MUST display an IES Scorecard that explicitly visualises the components: $Outcomes_i$, $W_{species}$, $W_{leverage}$, and $D_{evidence}$.
- **AND** the UI MUST clearly distinguish between empirical data (extracted from documents) and philosophical assumptions (EA moral weights and evidence discounts) via tooltips or distinct typography.