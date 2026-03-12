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

#### Scenario: Selective Rendering of Unspecified Beneficiaries
- **WHEN** rendering the ITN Scorecard or Impact Pathway on an individual organisation's page
- **THEN** the system MUST dynamically render the `unspecified` beneficiary type ONLY if its population is strictly greater than `0`.
- **AND** the original three types (`companion_animals`, `farmed_animals`, `wild_animals`) MUST continue to display by default (in grayscale if their population is 0).

#### Scenario: Hiding Unspecified Beneficiaries in Master Directory
- **WHEN** rendering the "Target Species (Neglectedness)" column in the Master Directory (`index.html`)
- **THEN** the UI MUST strictly evaluate and display only the original three types (`companion_animals`, `farmed_animals`, `wild_animals`).
- **AND** the `unspecified` type MUST remain entirely hidden from this view to preserve the column's comparative focus on EA cause areas, regardless of its population value.

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, dynamically suppressing the calculation if the data confidence is low.

#### Scenario: Suppressing Low Confidence Calculations on Profiles
- **WHEN** rendering the Value for Money component on a charity's individual profile
- **THEN** the template MUST check the `confidence_tier` of the `cost_per_outcome` metric.
- **AND** if `LOW`, it MUST hide the large numeric value and the retail donation translation, replacing it with a grey, subdued text box displaying the `confidence_note`.
- **AND** if `HIGH` or `MEDIUM`, it MUST display the calculated value, the retail translation, and append the `confidence_note` directly beneath it to ensure total transparency of the calculation's provenance.

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, normalising all financial inputs to USD to prevent user confusion, and rendering granular provenance.

#### Scenario: Rendering Line-Item Financial Provenance
- **WHEN** rendering the "Inputs" card (Total Annual Expenditure) or the "Value for Money" (Expense Breakdown) sections
- **THEN** the Hugo template MUST read the `.value` property of the respective financial figure.
- **AND** if a `.source` object is populated for that specific figure, the template MUST render the `provenance-badge.html` partial immediately adjacent to the printed figure, allowing users to verify individual income or expense metrics independently.

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

### Requirement: Interactive Provenance Badges
The UI SHALL render explicit, interactive citation badges for all quantitative figures and claims to facilitate immediate human verification against source documents.

#### Scenario: Rendering Document vs. Web Citations
- **WHEN** the Hugo template iterates over `beneficiaries`, `metrics`, `significant_events`, or `financials` that contain a populated `source` object
- **THEN** it MUST render a small UI badge adjacent to the claim (e.g., an icon with "📄 p. 12" for PDFs, or "🌐 Web" for web searches).
- **AND** the badge MUST be an anchor tag (`<a>`) linking to the `resolved_url`, ensuring the link opens in a new browser tab.
- **AND** the UI MUST expose the verbatim `quote` text either via a tooltip (e.g., standard `title` attribute) on the badge, or a collapsible `<details>` element beneath the claim, allowing the human reviewer to know exactly what text to scan for once the deep-link resolves.

