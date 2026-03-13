## MODIFIED Requirements

### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes.

#### Scenario: Displaying the Verified Leverage Portfolio
- **WHEN** rendering the "Tractability" card on the ITN Scorecard
- **THEN** the UI MUST label the block "Highest Intervention Leverage".
- **AND** it MUST parse the stringified JSON array in the `details.elaboration` field to dynamically render the complete verified portfolio of interventions, grouped by their respective Tiers.
- **AND** for every listed intervention, it MUST append an interactive `provenance-badge.html` using the exact source object provided in the payload, allowing users to verify the exact text validating that classification.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually.

#### Scenario: Intuitive Leverage Tier Presentation
- **WHEN** rendering the Tractability column in the Master Directory (now titled "Highest Leverage (Tractability)")
- **THEN** the UI MUST abstract the backend tier outputs into immediately understandable, colour-coded visual badges (e.g., Tier 1, Tier 2, Tier 3).
- **AND** the table's vanilla Javascript sorting logic MUST accurately sort these tiers hierarchically in descending order, where Tier 1 > Tier 2 > Tier 3 > Not Assessed.