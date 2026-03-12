## MODIFIED Requirements

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, normalising all financial inputs to USD to prevent user confusion, and rendering granular provenance.

#### Scenario: Rendering Line-Item Financial Provenance
- **WHEN** rendering the "Inputs" card (Total Annual Expenditure) or the "Value for Money" (Expense Breakdown) sections
- **THEN** the Hugo template MUST read the `.value` property of the respective financial figure.
- **AND** if a `.source` object is populated for that specific figure, the template MUST render the `provenance-badge.html` partial immediately adjacent to the printed figure, allowing users to verify individual income or expense metrics independently.