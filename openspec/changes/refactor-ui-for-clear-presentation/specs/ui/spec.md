## ADDED Requirements

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/audits/` directory
- **THEN** the system MUST display a Master Table listing all organizations.
- **AND** the table MUST include columns for: Organization Name, Target Species (Neglectedness), Evidence Quality (Tractability), Total Beneficiaries (Importance), and Cost per Outcome.
- **AND** the table MUST include a visual summary of the Audit Checklist (e.g., counts of Pass/Warn/Fail).
- **AND** clicking an organization's row or name MUST navigate the user to that organization's dedicated detail page.
- **AND** the table MUST be sortable via client-side JavaScript without requiring a backend connection.

## MODIFIED Requirements

### Requirement: Audit Checklist Presentation
*Note: This requirement's scope is updated to reflect the single-page architecture.*
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organization page.

#### Scenario: Isolated Organization Views
- **WHEN** a user navigates to an individual organization's URL
- **THEN** the UI MUST render the ITN Scorecard, Impact Pathway, Value for Money, and Audit Checklist exclusively for that specific organization.
- **AND** the page MUST include a "Back to Directory" navigation link to return to the Master Table.