## RENAMED Requirements
- FROM: `### Requirement: ITN Scorecard Rendering`
- TO: `### Requirement: Impact Profile Rendering`

## MODIFIED Requirements

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
The UI SHALL render the calculated Impact Equivalency Score (IES) in a dedicated component on the individual charity profile, explicitly framing it as an exploratory, temporally bounded model rather than an absolute truth.

#### Scenario: Contextualising the Score and its Ingredients
- **WHEN** rendering the IES Scorecard on a charity's profile page
- **THEN** the UI MUST include explanatory text making it clear to the audience that PRISM is exposing the "ingredients" of the calculation (empirical data vs. philosophical assumptions) for reference, rather than declaring a golden score.
- **AND** the UI MUST render an "Annual" badge (or similar temporal indicator) prominently within the scorecard header or near the final score to reinforce that the metric represents a single year's impact.
- **AND** the UI MUST visually balance the "Evaluated Impact" figure, ensuring its font size and weight do not disproportionately overshadow the underlying contextual breakdown or the "Claimed Impact".