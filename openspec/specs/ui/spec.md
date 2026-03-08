# ui Specification

## Purpose
This specification defines how the audit checklist is presented to the end-user. It ensures that charity effectiveness and risk data is rendered in a clear, transparent, and easily comparable "report card" format, displaying pass, fail, or warning statuses for each audit item.
## Requirements
### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes.

#### Scenario: Explicit Temporal Labelling on Scorecards
- **WHEN** rendering the Importance and Neglectedness sections of the scorecard
- **THEN** the UI MUST display a small, unobtrusive tag (e.g., "Annual") in the top-right corner of the respective cards.
- **AND** this tag MUST clearly indicate to the user that these specific metrics represent a single-year snapshot, preventing confusion with cumulative historical data.

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
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, dynamically suppressing the calculation if the data confidence is low.

#### Scenario: Suppressing Low Confidence Calculations on Profiles
- **WHEN** rendering the Value for Money component on a charity's individual profile
- **THEN** the template MUST check the `confidence_tier` of the `cost_per_outcome` metric.
- **AND** if `LOW`, it MUST hide the large numeric value and the retail donation translation, replacing it with a grey, subdued text box displaying the `confidence_note`.
- **AND** if `HIGH` or `MEDIUM`, it MUST display the calculated value, the retail translation, and append the `confidence_note` directly beneath it to ensure total transparency of the calculation's provenance.

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, normalising all financial inputs to USD to prevent user confusion.

#### Scenario: Rendering Normalized Inputs
- **WHEN** rendering the "Inputs" card (Total Annual Expenditure)
- **THEN** the Hugo template MUST dynamically multiply the raw total expenditure by the `usd_exchange_rate`.
- **AND** it MUST render the value with a "USD" prefix (e.g., "USD $50,000").
- **AND** it MUST include a hover tooltip indicating the original local currency amount and the exchange rate used (e.g., "Original: HKD $390,000 (Rate: 0.128 as of 2023-12-31)").

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organization page.

#### Scenario: Isolated Organization Views
- **WHEN** a user navigates to an individual organization's URL at the root level (e.g., `/<organization-slug>`)
- **THEN** the UI MUST render the ITN Scorecard, Impact Pathway, Value for Money, and Audit Checklist exclusively for that specific organization.
- **AND** the page MUST include a "Back to Directory" navigation link to return to the Master Table at the root path (`/`).

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually.

#### Scenario: Displaying Confidence Tiers in the Master Table
- **WHEN** rendering the "Cost per Outcome (USD)" column
- **THEN** if the `confidence_tier` is `LOW`, the UI MUST render "N/A" with a subtle warning tooltip explaining the multi-domain dilution.
- **AND** if the `confidence_tier` is `HIGH`, it MUST render the value next to a distinct icon (e.g., a solid checkmark) denoting an explicitly stated cost.
- **AND** if the `confidence_tier` is `MEDIUM`, it MUST render the value next to a distinct icon (e.g., a calculator) denoting a PRISM-calculated cost.
- **AND** the column MUST sort by the numeric unit cost for High/Medium values, pushing all "N/A" (Low Confidence) values to the bottom regardless of sort direction.

