# ui Specification

## Purpose
This specification defines the visual presentation of charity effectiveness data to the end-user, ensuring transparency and ease of comparison.
## Requirements
### Requirement: Priority-Sorted Audit Checklist
The UI SHALL display audit results as a vertical stack of expandable items, sorted by significance and pass/fail status.

#### Scenario: Displaying critical failures
- **GIVEN** a charity has failed a HIGH-significance check (e.g., Reserve Cap)
- **WHEN** the organisation page is loaded
- **THEN** this failure MUST be displayed at the top of the checklist.
- **AND** it MUST be highlighted with a critical (RED) visual treatment.

### Requirement: Expandable Transparency Details
Every audit check-item MUST be expandable to reveal the underlying data sources and formulas used for the result.

#### Scenario: Verifying a ratio
- **WHEN** a user expands the "Liquidity Ratio" item
- **THEN** the UI MUST display the specific HKD values used (e.g., Net Assets / Monthly Expenses) and the snippet from the source PDF.

### Requirement: Logic Model Path Visualization
The UI SHALL visualize the charity's impact pathway (Inputs -> Activities -> Outputs -> Outcomes).

#### Scenario: Visualizing the Theory of Change
- **WHEN** rendering the impact section
- **THEN** it SHALL display the causal chain.
- **AND** clearly distinguish between "Outputs" (e.g., people served) and "Outcomes" (e.g., lives improved).

