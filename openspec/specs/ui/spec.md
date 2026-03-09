# ui Specification

## Purpose
This specification defines how the audit checklist is presented to the end-user. It ensures that charity effectiveness and risk data is rendered in a clear, transparent, and easily comparable "report card" format, displaying pass, fail, or warning statuses for each audit item.
## Requirements
### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes.

#### Scenario: Displaying Intervention-Based Tractability
- **WHEN** rendering the "Tractability" card on the ITN Scorecard
- **THEN** the UI MUST derive the tractability score and description from the `analytics.check_items` array (specifically `check_intervention_tractability`), rather than parsing the `evidence_quality` from the raw impact metrics.
- **AND** it MUST display the highest matched EA evidence tier (e.g., "Quasi-Experimental") as the primary metric.
- **AND** it MUST display the EA rationale string (from the audit details) as the supporting text, replacing the charity's self-reported quote.

### Requirement: Data Provenance Indicators
The UI SHALL display the data sources used to generate the charity's evaluation to establish immediate transparency, including temporal bounding.

#### Scenario: Displaying the Financial Year
- **WHEN** rendering a charity's profile page and Impact Pathway
- **THEN** the UI MUST explicitly display the `financial_year` associated with the extracted data to ensure users understand the temporal snapshot of the financial metrics.

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

#### Scenario: Default Sorting Behaviour
- **WHEN** a user interacts with a sortable column header in the Master Directory for the first time
- **THEN** the table MUST sort the data in descending order (highest to lowest, or newest to oldest) to immediately surface the most impactful or relevant records.

