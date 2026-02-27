## ADDED Requirements

### Requirement: Charity Discovery Landing Page
The Hugo SSG SHALL generate a root index page displaying all evaluated charities, enabling cross-comparison without a backend.

#### Scenario: Rendering the Charity Roster
- **WHEN** a user visits the root URL (`/`)
- **THEN** the system MUST display a grid or list card for every charity present in the `data/organisations/` directory.
- **AND** each card MUST display the charity's name, primary beneficiary type, highest evidence quality, and overall risk level as data attributes (`data-risk`, `data-neglectedness`, `data-evidence`).

#### Scenario: Offline Client-Side Filtering
- **WHEN** the user interacts with "Sort by Neglectedness" or "Filter by Low Risk" UI controls on the landing page
- **THEN** a bundled, Vanilla JS script MUST dynamically hide/show or reorder the charity cards based on their DOM data attributes.
- **AND** this action MUST NOT require any network requests, adhering to the project's Offline Sovereignty constraint.