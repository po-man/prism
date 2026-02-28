## MODIFIED Requirements

### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, dynamically calculating and displaying proportional beneficiary breakdowns from raw population data.

#### Scenario: Displaying Species Neglectedness Portions
- **WHEN** rendering the Neglectedness section of the scorecard
- **THEN** the UI MUST explicitly display the primary animal beneficiary type (Companion vs. Farmed vs. Wild) and provide a visual indicator of its neglectedness relative to the overall HK philanthropic landscape.
- **AND** the UI MUST compute the total population by summing `.population` for all entries in the `.impact.data.beneficiaries` array.
- **AND** if the total population > 0, it MUST calculate the percentage representing each `beneficiary_type`.
- **AND** it MUST render the calculated percentage alongside the respective beneficiary badges (e.g., `Companion Animals (80%)` and `Wild Animals (20%)`).
- **AND** if population data is `null` or 0, it MUST render the badges based on presence/absence without percentages, leaving absent categories greyed out (`opacity-40 grayscale`).