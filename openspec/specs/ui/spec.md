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
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, dynamically suppressing the calculation if the data confidence is low.

#### Scenario: Rendering Arrays of Intervention-Specific Costs
- **WHEN** rendering the Value for Money component on a charity's individual profile (`myth-buster.html`)
- **THEN** the template MUST parse the `cost_per_outcome` metric to determine if multiple intervention-specific costs were identified (e.g., from the `explicit_unit_costs` array).
- **AND** if multiple costs exist, it MUST render them as a list, displaying the specific intervention name (e.g., "High Volume Spay Neuter: $25", "Individual Rescue: $450") instead of a single blended number.
- **AND** if the metric was derived via the Pure-Play cohort logic, it MUST display a specific badge or text indicating it as a "Pure-Play Benchmark".

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, normalising all financial inputs to USD to prevent user confusion, whilst maintaining full data provenance via tooltips.

#### Scenario: Rendering Normalized Inputs with Scaling Context
- **WHEN** rendering the "Inputs" card (Total Annual Expenditure)
- **THEN** the underlying Hugo template MUST compute the true local value by multiplying the raw `.value` by the `.scale_multiplier`.
- **AND** the hover tooltip MUST reflect the mathematically scaled local currency for maximum transparency (e.g., "Original: HKD 20,000,000 (Extracted as 20 x 1,000,000). Rate: 0.128").

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organization page.

#### Scenario: Rendering Advanced Check Statuses
- **WHEN** rendering items in the Audit Checklist (`audit-checklist.html`)
- **THEN** the template MUST map the `bonus` status to a distinct positive visual indicator (e.g., a purple dot and `bg-purple-100` background).
- **AND** it MUST map `not_disclosed` and `n_a` statuses to a neutral visual indicator (e.g., a grey dot and `bg-gray-100` background).
- **AND** the internal sorting logic MUST place `bonus` items at the top of their respective category blocks, followed by `pass`, `warning`, `fail`, `not_disclosed`, and `n_a`.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually while avoiding over-simplified hierarchical rankings.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/` directory (Landing Page)
- **THEN** the system MUST display a Master Table listing all organizations.
- **AND** the table MUST include columns for: Organization Name, Data Sources, Target Species (Neglectedness), Total Beneficiaries (Importance), Cost per Outcome (USD), and Audit Summary.
- **AND** the table MUST NOT include the "Highest Leverage (Tractability)" column.
- **AND** clicking an organization's row or name MUST navigate the user to that organization's dedicated detail page at the URL path `/<slug>`.
- **AND** the table MUST remain sortable via client-side JavaScript, utilizing hidden `data-sort-value` attributes.

### Requirement: Interactive Provenance Badges
The UI SHALL render explicit, interactive citation badges for all quantitative figures and claims to facilitate immediate human verification against source documents.

#### Scenario: Rendering Document Citations
- **WHEN** the Hugo template iterates over `beneficiaries`, `metrics`, `significant_events`, or `financials` that contain a populated `source` object
- **THEN** it MUST render a small UI badge adjacent to the claim (e.g., an icon with "📄 p. 12" for PDFs).
- **AND** it MUST NOT check for or render web search specific formatting or icons.

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score (IES) in a dedicated component on the individual charity profile, explicitly framing it as an exploratory, temporally bounded model rather than an absolute truth.

#### Scenario: Contextualising the Score and its Ingredients
- **WHEN** rendering the IES Scorecard on a charity's profile page
- **THEN** the UI MUST include explanatory text making it clear to the audience that PRISM is exposing the "ingredients" of the calculation (empirical data vs. philosophical assumptions) for reference, rather than declaring a golden score.
- **AND** the UI MUST render an "Annual" badge (or similar temporal indicator) prominently within the scorecard header or near the final score to reinforce that the metric represents a single year's impact.
- **AND** the UI MUST visually balance the "Evaluated Impact" figure, ensuring its font size and weight do not disproportionately overshadow the underlying contextual breakdown or the "Claimed Impact".

### Requirement: Impact Profile Rendering
The static site generator (Hugo) SHALL render an Impact Profile for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes, adopting layman demographic terminology, and visually separating programmatic scale from intervention types.

#### Scenario: Translating EA Terminology to Layman Demographics
- **WHEN** rendering the top-level metric cards for "Importance" and "Neglectedness"
- **THEN** the UI MUST replace EA-specific jargon with public-friendly, demographic-focused titles (e.g., "Scale of Reach" instead of Importance, and "Beneficiary Demographics" instead of Neglectedness).

#### Scenario: Visual Hierarchy and Layout Restructuring
- **WHEN** rendering the Impact Profile grid layout
- **THEN** the UI MUST position the demographic cards ("Scale of Reach" and "Beneficiary Demographics") together on the primary, top row.
- **AND** the UI MUST isolate the interventions component on a secondary, full-width row beneath the demographic data to improve readability and visual flow.

#### Scenario: Displaying a Deduplicated Intervention Portfolio
- **WHEN** rendering the secondary row on the Impact Profile
- **THEN** the UI MUST label the block "Intervention Portfolio".
- **AND** it MUST parse the stringified JSON array in the `details.elaboration` field to dynamically render the verified portfolio of interventions.
- **AND** the UI MUST programmatically deduplicate the interventions to ensure each unique intervention name is only listed once.
- **AND** the UI MUST visually present these unique interventions as an accessible cluster of tags or badges, entirely removing the prominent display of the "Tier" hierarchy.

