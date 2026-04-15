## MODIFIED Requirements

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score ($IES$) in a dedicated, self-explanatory component on the individual charity profile, breaking down the deterministic variables used in the calculation.

#### Scenario: Rendering Claimed vs. Evaluated Impact
- **WHEN** rendering the IES Scorecard on a charity's profile page
- **THEN** the UI MUST prominently present the **"Claimed IES"** (representing the charity's raw impact claim without epistemic discounts).
- **AND** it MUST overlay or distinctly display the **"Epistemic Confidence Rating"** (the $D_{evidence}$ discount applied).
- **AND** it MUST render the final **"Evaluated IES"** as the product of the Claimed IES and the Epistemic Confidence Rating, validating the charity's hard work whilst retaining an objective EA expected-value lens.