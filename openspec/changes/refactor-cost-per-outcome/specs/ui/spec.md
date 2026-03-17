## MODIFIED Requirements

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, dynamically suppressing the calculation if the data confidence is low.

#### Scenario: Rendering Sparse Unit Costs on Individual Profiles
- **WHEN** rendering the "Value for Money" component on a charity's individual profile (`myth-buster.html`)
- **THEN** the template MUST loop through all `calculated_metrics` whose ID starts with `cost_per_outcome:`.
- **AND** it MUST render a distinct card or section for each calculated intervention cost, clearly labelling the intervention type (e.g., "Estimated Cost per Spay/Neuter").
- **AND** if only a `LOW` confidence blended metric exists (i.e., ID `cost_per_outcome`), it MUST fallback to displaying the grey, subdued text box with the `confidence_note` explaining why a unit cost could not be accurately calculated.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually.

#### Scenario: Displaying Intervention Badges and Costs in the Master Directory
- **WHEN** rendering the cost column in the Master Directory (`index.html`)
- **THEN** the column header MUST be renamed to "Key Interventions & Unit Costs".
- **AND** the UI MUST dynamically generate visual badges for each intervention category where a unit cost was attempted.
- **AND** if a `HIGH` or `MEDIUM` confidence cost was calculated, the cost (e.g., "$25") MUST be rendered alongside the corresponding badge icon.
- **AND** if the calculation was aborted (`LOW` confidence), the badge MUST still render to indicate the charity performs this work, but with an "N/A" or missing indicator for the cost, ensuring users see *what* the charity does even if financial transparency prevents a cost calculation.
- **AND** the table's vanilla JavaScript sorting logic MUST be updated to accommodate this sparse matrix, potentially sorting by the presence of high-leverage badges or sorting explicitly by the unit cost of a user-selected intervention type.