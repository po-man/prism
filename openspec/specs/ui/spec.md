# ui Specification

## Purpose
This specification defines how the audit checklist is presented to the end-user. It ensures that charity effectiveness and risk data is rendered in a clear, transparent, and easily comparable "report card" format, displaying pass, fail, or warning statuses for each audit item.
## Requirements
### Requirement: Data Provenance Indicators
The UI SHALL display the data sources used to generate the charity's evaluation to establish immediate transparency, including temporal bounding, strictly limited to formal documentation.

#### Scenario: Displaying the Financial Year and Attached Reports
- **WHEN** rendering a charity's profile page and Impact Pathway
- **THEN** the UI MUST explicitly display the `financial_year` associated with the extracted data.
- **AND** it MUST ONLY display provenance icons for the "Annual Report" and "Financial Report".
- **AND** it MUST NOT render any visual indicators or icons suggesting web searches were performed.

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
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, contextualizing administrative overhead with the absolute total financial inputs.

#### Scenario: Integrating Total Annual Expenditure
- **WHEN** rendering the Expense Breakdown column within the Value for Money section
- **THEN** the UI MUST dynamically calculate and render the Total Annual Expenditure in USD at the top of the card.
- **AND** it MUST include the original local currency and exchange rate as a hover-able tooltip on the total figure.

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organisation page.

#### Scenario: Exposing Audit Evaluation Rules
- **WHEN** a user clicks to expand a `<details>` element in the Audit Checklist
- **THEN** the expanded area MUST cleanly separate into a top "Evaluation Criteria" block and a bottom "Result" block.
- **AND** the top block MUST render the `details.criteria` string provided by the audit engine, styled with a muted background (e.g., `bg-gray-50`) to indicate it is a static rule.
- **AND** the bottom block MUST render the charity-specific `details.calculation` and `details.elaboration` (rendered as an italicised blockquote) to show how they performed against the rule.
- **AND** all hardcoded threshold tooltips (`$tooltips` dictionary) MUST be removed from the Hugo template.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, avoiding over-simplified hierarchical rankings and academic jargon.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/` directory (Landing Page)
- **THEN** the system MUST display a Master Table listing all organisations.
- **AND** the column headers MUST use layman terminology, explicitly avoiding jargon such as "(Neglectedness)" and "(Importance)".
- **AND** the "Target Species" column MUST visually indicate the proportionate breakdown of beneficiaries using species-specific SVG icons, explicitly including the `unspecified` beneficiary type alongside companion, farmed, and wild animals, mapping the percentage to the visual opacity.

### Requirement: Interactive Provenance Badges
The UI SHALL render explicit, interactive citation badges for all quantitative figures and claims to facilitate immediate human verification against source documents.

#### Scenario: Rendering Document Citations
- **WHEN** the Hugo template iterates over `beneficiaries`, `metrics`, `significant_events`, or `financials` that contain a populated `source` object
- **THEN** it MUST render a small UI badge adjacent to the claim (e.g., an icon with "📄 p. 12" for PDFs).
- **AND** it MUST NOT check for or render web search specific formatting or icons.

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score (IES) in a dedicated component on the individual charity profile, explicitly framing it as an exploratory, temporally bounded model.

#### Scenario: Simplifying the Header
- **WHEN** rendering the IES Scorecard header
- **THEN** the UI MUST NOT display redundant "Annual" tags, streamlining the visual interface.

### Requirement: Impact Profile Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence.

#### Scenario: Visualising Intervention Tractability Tiers
- **WHEN** rendering the Tractability section ("Intervention Portfolio") of the scorecard
- **THEN** the UI MUST group and display the verified interventions as badges.
- **AND** the UI MUST dynamically apply distinct colour schemes to the badges based on their Leverage Tier (e.g., Tier 1: Purple, Tier 2: Blue, Tier 3: Grey).
- **AND** the UI MUST render a contextual key beneath the portfolio explaining the colour mapping to the respective tiers.
- **AND** the UI MUST NOT display redundant "Annual" tags on the scorecard headers, assuming the report's temporal bounding is globally understood.

