# ui Specification

## Purpose
This specification defines how the audit checklist is presented to the end-user. It ensures that charity effectiveness and risk data is rendered in a clear, transparent, and easily comparable "report card" format, displaying pass, fail, or warning statuses for each audit item.
## Requirements
### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes.

#### Scenario: Displaying the Verified Leverage Portfolio
- **WHEN** rendering the "Tractability" card on the ITN Scorecard
- **THEN** the UI MUST label the block "Highest Intervention Leverage".
- **AND** it MUST parse the stringified JSON array in the `details.elaboration` field to dynamically render the complete verified portfolio of interventions, grouped by their respective Tiers.
- **AND** for every listed intervention, it MUST append an interactive `provenance-badge.html` using the exact source object provided in the payload, allowing users to verify the exact text validating that classification.

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

#### Scenario: Rendering Arrays of Intervention-Specific Costs
- **WHEN** rendering the Value for Money component on a charity's individual profile (`myth-buster.html`)
- **THEN** the template MUST parse the `cost_per_outcome` metric to determine if multiple intervention-specific costs were identified (e.g., from the `explicit_unit_costs` array).
- **AND** if multiple costs exist, it MUST render them as a list, displaying the specific intervention name (e.g., "High Volume Spay Neuter: $25", "Individual Rescue: $450") instead of a single blended number.
- **AND** if the metric was derived via the Pure-Play cohort logic, it MUST display a specific badge or text indicating it as a "Pure-Play Benchmark".

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, normalising all financial inputs to USD to prevent user confusion, and rendering granular provenance.

#### Scenario: Rendering Line-Item Financial Provenance
- **WHEN** rendering the "Inputs" card (Total Annual Expenditure) or the "Value for Money" (Expense Breakdown) sections
- **THEN** the Hugo template MUST read the `.value` property of the respective financial figure.
- **AND** if a `.source` object is populated for that specific figure, the template MUST render the `provenance-badge.html` partial immediately adjacent to the printed figure, allowing users to verify individual income or expense metrics independently.

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organization page.

#### Scenario: Rendering Advanced Check Statuses
- **WHEN** rendering items in the Audit Checklist (`audit-checklist.html`)
- **THEN** the template MUST map the `bonus` status to a distinct positive visual indicator (e.g., a purple dot and `bg-purple-100` background).
- **AND** it MUST map `not_disclosed` and `n_a` statuses to a neutral visual indicator (e.g., a grey dot and `bg-gray-100` background).
- **AND** the internal sorting logic MUST place `bonus` items at the top of their respective category blocks, followed by `pass`, `warning`, `fail`, `not_disclosed`, and `n_a`.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually.

#### Scenario: Including Bonuses in the Audit Summary Column
- **WHEN** rendering the "Audit Summary" column in the Master Directory (`index.html`)
- **THEN** the UI MUST parse and display the count of `bonus` checks achieved by the organisation alongside the existing pass/warn/fail counts.
- **AND** the vanilla JavaScript table sorting logic MUST be updated to account for the bonus count, prioritizing organisations with a higher number of bonuses when sorted descending (best to worst).

### Requirement: Interactive Provenance Badges
The UI SHALL render explicit, interactive citation badges for all quantitative figures and claims to facilitate immediate human verification against source documents.

#### Scenario: Rendering Document vs. Web Citations
- **WHEN** the Hugo template iterates over `beneficiaries`, `metrics`, `significant_events`, or `financials` that contain a populated `source` object
- **THEN** it MUST render a small UI badge adjacent to the claim (e.g., an icon with "📄 p. 12" for PDFs, or "🌐 Web" for web searches).
- **AND** the badge MUST be an anchor tag (`<a>`) linking to the `resolved_url`, ensuring the link opens in a new browser tab.
- **AND** the UI MUST expose the verbatim `quote` text either via a tooltip (e.g., standard `title` attribute) on the badge, or a collapsible `<details>` element beneath the claim, allowing the human reviewer to know exactly what text to scan for once the deep-link resolves.

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score ($IES$) in a dedicated, self-explanatory component on the individual charity profile, breaking down the deterministic variables used in the calculation.

#### Scenario: Visualising the IES Formula
- **WHEN** rendering a charity's profile page
- **THEN** the Hugo template MUST display an IES Scorecard that explicitly visualises the components: $Outcomes_i$, $W_{species}$, $W_{leverage}$, and $D_{evidence}$.
- **AND** the UI MUST clearly distinguish between empirical data (extracted from documents) and philosophical assumptions (EA moral weights and evidence discounts) via tooltips or distinct typography.

