## MODIFIED Requirements

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually.

#### Scenario: Displaying Confidence Tiers in the Master Table
- **WHEN** rendering the "Cost per Outcome (USD)" column
- **THEN** if the `confidence_tier` is `LOW`, the UI MUST render "N/A" with a subtle warning tooltip explaining the multi-domain dilution.
- **AND** if the `confidence_tier` is `HIGH`, it MUST render the value next to a distinct icon (e.g., a solid checkmark) denoting an explicitly stated cost.
- **AND** if the `confidence_tier` is `MEDIUM`, it MUST render the value next to a distinct icon (e.g., a calculator) denoting a PRISM-calculated cost.
- **AND** the column MUST sort by the numeric unit cost for High/Medium values, pushing all "N/A" (Low Confidence) values to the bottom regardless of sort direction.

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, dynamically suppressing the calculation if the data confidence is low.

#### Scenario: Suppressing Low Confidence Calculations on Profiles
- **WHEN** rendering the Value for Money component on a charity's individual profile
- **THEN** the template MUST check the `confidence_tier` of the `cost_per_outcome` metric.
- **AND** if `LOW`, it MUST hide the large numeric value and the retail donation translation, replacing it with a grey, subdued text box displaying the `confidence_note`.
- **AND** if `HIGH` or `MEDIUM`, it MUST display the calculated value, the retail translation, and append the `confidence_note` directly beneath it to ensure total transparency of the calculation's provenance.