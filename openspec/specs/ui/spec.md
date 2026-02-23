# ui Specification

## Purpose
This specification defines the visual presentation of charity effectiveness data to the end-user, ensuring transparency and ease of comparison.
## Requirements
### Requirement: Priority-Sorted Audit Checklist
The UI SHALL display audit results as a vertical stack of expandable items, sorted by category, then by significance, and then by pass/fail status.

#### Scenario: Displaying categorical check-items
- **GIVEN** a charity has been audited across Financial Health, Governance, and Impact Awareness categories
- **WHEN** the organisation page is loaded
- **THEN** the UI MUST group the results under distinct section headers for each category.
- **AND** within each category, failures of HIGH-significance MUST be displayed at the top of the list.

### Requirement: Expandable Transparency Details
Every audit check-item MUST be expandable to reveal the underlying data sources and formulas used for the result.

#### Scenario: Verifying a ratio
- **WHEN** a user expands the "Liquidity Ratio" item
- **THEN** the UI MUST display the specific HKD values used (e.g., Net Assets / Monthly Expenses) and the snippet from the source PDF.

### Requirement: Logic Model Path Visualization
The UI SHALL visualize the charity's impact pathway (Inputs -> Activities -> Outputs -> Outcomes).

#### Scenario: Visualizing the Theory of Change
- **WHEN** rendering the impact section
- **THEN** it SHALL display the causal chain horizontally or vertically.
- **AND** clearly distinguish between "Outputs" (e.g., people served) and "Outcomes" (e.g., lives improved).
- **AND** MUST prominently display the counterfactual baseline to highlight the marginal impact of the organization's existence.

### Requirement: ITN Scorecard Visualization
The UI SHALL present a top-level summary of the charity's profile using the Importance, Tractability, and Neglectedness (ITN) framework to immediately anchor the user in impact-oriented thinking.

#### Scenario: Rendering the ITN Scorecard
- **WHEN** a user visits a charity's profile page
- **THEN** the UI MUST display the ITN Scorecard containing the problem scale, the highest quality of evidence used, and a visual breakdown of funding sources.

### Requirement: Value for Money Contextualization
The UI SHALL actively contextualize administrative overhead ratios by pairing them visually with outcome-based metrics, preventing users from making decisions based solely on financial efficiency.

#### Scenario: Displaying the Myth-Buster Component
- **WHEN** rendering the financial efficiency section
- **THEN** the UI MUST display the program-to-admin ratio adjacent to the "Estimated Cost per Outcome" metric.
- **AND** MUST include an educational disclaimer clarifying that low overhead does not equate to high impact.

