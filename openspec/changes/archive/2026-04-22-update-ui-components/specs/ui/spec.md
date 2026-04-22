## MODIFIED Requirements

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, dynamically suppressing the calculation if the data confidence is low.

#### Scenario: Missing Expense Data Fallback
- **WHEN** rendering the Expense Breakdown column on a charity's individual profile (`myth-buster.html`)
- **THEN** the UI MUST always render the component structure to maintain visual symmetry with the Cost per Outcome column.
- **AND** if total expenditure data is `nil` or unavailable, it MUST display a greyed-out placeholder indicating missing data, mirroring the visual style of the "Not Calculated" state.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually while avoiding over-simplified hierarchical rankings.

#### Scenario: Proportional Audit Summary Opacity
- **WHEN** rendering the "Audit Summary" column in the Master Table
- **THEN** the UI MUST dynamically adjust the opacity of the pass, warning, and fail indicator dots.
- **AND** the opacity MUST scale proportionally based on the number of checks in each category over the total number of checks, using a baseline minimum opacity of 20% and a maximum of 100% (e.g., `(Count / Total * 0.8) + 0.2`).

### Requirement: Impact Profile Rendering
The static site generator (Hugo) SHALL render an Impact Profile for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes, adopting layman demographic terminology, and visually separating programmatic scale from intervention types.

#### Scenario: Displaying a Deduplicated Intervention Portfolio
- **WHEN** rendering the "Intervention Portfolio" block on the Impact Profile
- **THEN** the UI MUST label the block "Intervention Portfolio".
- **AND** it MUST parse the stringified JSON array in the `details.elaboration` field to dynamically render the verified portfolio of interventions.
- **AND** the UI MUST programmatically deduplicate the interventions to ensure each unique intervention name is only listed once.
- **AND** the UI MUST visually present these unique interventions as an accessible cluster of tags or badges, entirely removing the prominent display of the "Tier" hierarchy.
- **AND** it MUST cap the number of interactive provenance badges rendered alongside each intervention name to a maximum of 3, preventing visual clutter.