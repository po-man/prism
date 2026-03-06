# ui Specification

## Purpose
This specification defines how the audit checklist is presented to the end-user. It ensures that charity effectiveness and risk data is rendered in a clear, transparent, and easily comparable "report card" format, displaying pass, fail, or warning statuses for each audit item.
## Requirements
### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence.

#### Scenario: Displaying Cumulative Importance and Verifiable Tractability
- **WHEN** rendering the Importance section of the scorecard
- **THEN** the UI MUST compute and display the sum total of all populations across the `.impact.data.beneficiaries` array.
- **AND** it MUST explicitly display the demographic breakdown (e.g., specific species or beneficiary types) directly beneath the total "Affects up to X individuals" metric.
- **WHEN** rendering the Tractability section of the scorecard
- **THEN** the UI MUST display the highest `evidence_quality` achieved.
- **AND** it MUST display the exact `evidence_quote` associated with that metric to verify the claim, or provide an elaboration if a direct quote is unavailable.

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
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, pulling from dedicated calculation entities.

#### Scenario: Rendering Decoupled Calculations
- **WHEN** rendering the Value for Money component
- **THEN** the template MUST extract the Cost per Outcome data directly from the new `analytics.calculated_metrics` array, rather than parsing it out of the `check_items` array.

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, prioritizing the most significant interventions to prevent cognitive overload, and providing direct, highlighted verification links for web-sourced claims.

#### Scenario: Expanding Top 3 Interventions
- **WHEN** rendering the "Activities & Outputs" and "Outcomes" columns
- **THEN** the UI MUST sort the items by significance (based on the array order provided by the LLM).
- **AND** it MUST display only the top 3 items by default.
- **AND** if more than 3 items exist, it MUST provide an interactive, offline-compatible toggle (e.g., "Show all X activities") to reveal the remaining items.

#### Scenario: Hyperlinking and Highlighting Web-Sourced Claims
- **WHEN** rendering the "Activities & Outputs" and "Outcomes" items in the Impact Pathway
- **THEN** the UI MUST check for the presence of the `source_url` field.
- **AND** if `source_url` is present, it MUST wrap the `metric_name` (or the `event_name`) in an HTML `<a>` tag with `target="_blank"` and `rel="noopener noreferrer"`.
- **AND** if an exact quote (`source_quote` or `evidence_quote`) is also present, the UI MUST URL-encode the quote and append it to the `href` using the W3C Text Fragment syntax (`#:~:text=`), ensuring the user's browser automatically scrolls to and highlights the claim.

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organization page.

#### Scenario: Isolated Organization Views
- **WHEN** a user navigates to an individual organization's URL at the root level (e.g., `/<organization-slug>`)
- **THEN** the UI MUST render the ITN Scorecard, Impact Pathway, Value for Money, and Audit Checklist exclusively for that specific organization.
- **AND** the page MUST include a "Back to Directory" navigation link to return to the Master Table at the root path (`/`).

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/` directory (Landing Page)
- **THEN** the system MUST display a Master Table listing all organizations.
- **AND** the table MUST include columns for: Organization Name, Data Sources, Target Species (Neglectedness), Total Beneficiaries (Importance), Evidence Quality (Tractability), Cost per Outcome, and Audit Summary.
- **AND** the "Data Sources" column MUST display icons for Annual Report, Financial Report, and Web Search, greying out missing sources.
- **AND** the "Target Species" column MUST visually indicate the proportionate breakdown of beneficiaries using species-specific SVG icons, mapping the percentage of each species to the visual opacity of its icon (or greying out absent species).
- **AND** clicking an organization's row or name MUST navigate the user to that organization's dedicated detail page at the URL path `/<slug>`.
- **AND** the table MUST remain sortable via client-side JavaScript, utilizing hidden `data-sort-value` attributes for columns containing complex HTML (like the new icon arrays).

