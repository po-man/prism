## MODIFIED Requirements

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