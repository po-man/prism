## MODIFIED Requirements

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, normalising all financial inputs to USD to prevent user confusion, whilst maintaining full data provenance via tooltips.

#### Scenario: Rendering Normalized Inputs with Scaling Context
- **WHEN** rendering the "Inputs" card (Total Annual Expenditure)
- **THEN** the underlying Hugo template MUST compute the true local value by multiplying the raw `.value` by the `.scale_multiplier`.
- **AND** the hover tooltip MUST reflect the mathematically scaled local currency for maximum transparency (e.g., "Original: HKD 20,000,000 (Extracted as 20 x 1,000,000). Rate: 0.128").