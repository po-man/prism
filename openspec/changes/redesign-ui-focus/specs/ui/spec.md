## RENAMED Requirements
- FROM: `### Requirement: ITN Scorecard Rendering`
- TO: `### Requirement: Impact Profile Rendering`

## MODIFIED Requirements

### Requirement: Impact Profile Rendering
The static site generator (Hugo) SHALL render an Impact Profile for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes and de-emphasising rigid EA terminology.

#### Scenario: Displaying Verified Activities without Tiered Hierarchy
- **WHEN** rendering the middle card (formerly Tractability) on the Impact Profile
- **THEN** the UI MUST label the block "Verified Interventions" or "Verified Activities".
- **AND** it MUST parse the stringified JSON array in the `details.elaboration` field to dynamically render the complete verified portfolio of interventions.
- **AND** the UI MUST visually present these interventions as an accessible cluster of tags or badges, explicitly removing the prominent display of the specific "Tier 1/2/3" hierarchy from the top-level metric readout.
- **AND** for every listed intervention, it MUST append an interactive `provenance-badge.html` using the exact source object provided in the payload.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually while avoiding over-simplified hierarchical rankings.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/` directory (Landing Page)
- **THEN** the system MUST display a Master Table listing all organizations.
- **AND** the table MUST include columns for: Organization Name, Data Sources, Target Species (Neglectedness), Total Beneficiaries (Importance), Cost per Outcome (USD), and Audit Summary.
- **AND** the table MUST NOT include the "Highest Leverage (Tractability)" column.
- **AND** clicking an organization's row or name MUST navigate the user to that organization's dedicated detail page at the URL path `/<slug>`.
- **AND** the table MUST remain sortable via client-side JavaScript, utilizing hidden `data-sort-value` attributes.

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score (IES) in a dedicated component on the individual charity profile, explicitly framing it as an exploratory model rather than an absolute truth by breaking down the deterministic variables used in the calculation.

#### Scenario: Contextualising the Score and its Ingredients
- **WHEN** rendering the IES Scorecard on a charity's profile page
- **THEN** the UI MUST include explanatory text making it clear to the audience that PRISM is exposing the "ingredients" of the calculation (empirical data vs. philosophical assumptions) for reference, rather than declaring a golden score.
- **AND** the UI MUST visually balance the "Evaluated Impact" figure, ensuring its font size and weight do not disproportionately overshadow the underlying contextual breakdown or the "Claimed Impact".