## MODIFIED Requirements

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/` directory (Landing Page)
- **THEN** the system MUST display a Master Table listing all organizations.
- **AND** the table MUST include columns for: Organization Name, Data Sources, Target Species (Neglectedness), Total Beneficiaries (Importance), Evidence Quality (Tractability), Cost per Outcome, and Audit Summary.
- **AND** the "Data Sources" column MUST display icons for Annual Report, Financial Report, and Web Search, greying out missing sources.
- **AND** the "Target Species" column MUST visually indicate the proportionate breakdown of beneficiaries using species-specific SVG icons, mapping the percentage of each species to the visual opacity of its icon (or greying out absent species).
- **AND** clicking an organization's row or name MUST navigate the user to that organization's dedicated detail page at the URL path `/<slug>`.
- **AND** the table MUST remain sortable via client-side JavaScript, utilizing hidden `data-sort-value` attributes for columns containing complex HTML (like the new icon arrays).

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organization page.

#### Scenario: Isolated Organization Views
- **WHEN** a user navigates to an individual organization's URL at the root level (e.g., `/<organization-slug>`)
- **THEN** the UI MUST render the ITN Scorecard, Impact Pathway, Value for Money, and Audit Checklist exclusively for that specific organization.
- **AND** the page MUST include a "Back to Directory" navigation link to return to the Master Table at the root path (`/`).