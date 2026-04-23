## MODIFIED Requirements

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, avoiding over-simplified hierarchical rankings and academic jargon.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/` directory (Landing Page)
- **THEN** the system MUST display a Master Table listing all organisations.
- **AND** the column headers MUST use layman terminology, explicitly avoiding jargon such as "(Neglectedness)" and "(Importance)".
- **AND** the "Target Species" column MUST visually indicate the proportionate breakdown of beneficiaries using species-specific SVG icons, explicitly including the `unspecified` beneficiary type alongside companion, farmed, and wild animals, mapping the percentage to the visual opacity.

### Requirement: Impact Profile Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence.

#### Scenario: Visualising Intervention Tractability Tiers
- **WHEN** rendering the Tractability section ("Intervention Portfolio") of the scorecard
- **THEN** the UI MUST group and display the verified interventions as badges.
- **AND** the UI MUST dynamically apply distinct colour schemes to the badges based on their Leverage Tier (e.g., Tier 1: Purple, Tier 2: Blue, Tier 3: Grey).
- **AND** the UI MUST render a contextual key beneath the portfolio explaining the colour mapping to the respective tiers.
- **AND** the UI MUST NOT display redundant "Annual" tags on the scorecard headers, assuming the report's temporal bounding is globally understood.

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score (IES) in a dedicated component on the individual charity profile, explicitly framing it as an exploratory, temporally bounded model.

#### Scenario: Simplifying the Header
- **WHEN** rendering the IES Scorecard header
- **THEN** the UI MUST NOT display redundant "Annual" tags, streamlining the visual interface.