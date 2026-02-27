# ui Specification

## Purpose
This specification defines how the audit checklist is presented to the end-user. It ensures that charity effectiveness and risk data is rendered in a clear, transparent, and easily comparable "report card" format, displaying pass, fail, or warning statuses for each audit item.
## Requirements
### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity.

#### Scenario: Displaying Species Neglectedness
- **WHEN** rendering the Neglectedness section of the scorecard
- **THEN** the UI MUST explicitly display the primary animal beneficiary type (Companion vs. Farmed vs. Wild) and provide a visual indicator of its neglectedness relative to the overall HK philanthropic landscape.

