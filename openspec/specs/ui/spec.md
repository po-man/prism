# ui Specification

## Purpose
This specification defines how the audit checklist is presented to the end-user. It ensures that charity effectiveness and risk data is rendered in a clear, transparent, and easily comparable "report card" format, displaying pass, fail, or warning statuses for each audit item.
## Requirements
### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, dynamically calculating and displaying proportional beneficiary breakdowns from raw population data.

#### Scenario: Displaying Species Neglectedness Portions
- **WHEN** rendering the Neglectedness section of the scorecard
- **THEN** the UI MUST explicitly display the primary animal beneficiary type (Companion vs. Farmed vs. Wild) and provide a visual indicator of its neglectedness relative to the overall HK philanthropic landscape.
- **AND** the UI MUST compute the total population by summing `.population` for all entries in the `.impact.data.beneficiaries` array.
- **AND** if the total population > 0, it MUST calculate the percentage representing each `beneficiary_type`.
- **AND** it MUST render the calculated percentage alongside the respective beneficiary badges (e.g., `Companion Animals (80%)` and `Wild Animals (20%)`).
- **AND** if population data is `null` or 0, it MUST render the badges based on presence/absence without percentages, leaving absent categories greyed out (`opacity-40 grayscale`).

### Requirement: Data Provenance Indicators
The UI SHALL display the data sources used to generate the charity's evaluation to establish immediate transparency.

#### Scenario: Rendering available and missing sources
- **WHEN** rendering a charity's profile page
- **THEN** the system MUST display an icon row indicating the status of the "Annual Report", "Financial Report", and "Web Search".
- **AND** if the `annual_report` or `financial_report` ID is `null` or missing in the JSON data, the respective icon MUST be rendered in a disabled, greyed-out, or struck-through state.

### Requirement: Animal Beneficiary Badges
The UI SHALL visually categorize the charity's beneficiaries to immediately communicate cause-area neglectedness.

#### Scenario: Displaying beneficiary taxonomy
- **WHEN** rendering the ITN Scorecard or Impact Pathway
- **THEN** the system MUST parse the `impact.data.beneficiaries` array.
- **AND** map the `beneficiary_type` values (`companion_animals`, `farmed_animals`, `wild_animals`) to distinct SVG icons or badges, displaying them prominently to the user.

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent.

#### Scenario: Displaying the $1,000 Retail Translator
- **WHEN** rendering the "Estimated Cost per Outcome" block in the Value for Money section
- **THEN** the UI MUST display the raw calculated cost per outcome.
- **AND** it MUST additionally display a translated metric showing exactly what a $1,000 HKD donation achieves (e.g., "A $1,000 donation achieves ≈ 4.2 outcomes"), extracting this string from the updated audit check details.

