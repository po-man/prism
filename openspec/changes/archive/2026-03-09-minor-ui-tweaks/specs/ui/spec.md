## MODIFIED Requirements

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually.

#### Scenario: Default Sorting Behaviour
- **WHEN** a user interacts with a sortable column header in the Master Directory for the first time
- **THEN** the table MUST sort the data in descending order (highest to lowest, or newest to oldest) to immediately surface the most impactful or relevant records.

### Requirement: Data Provenance Indicators
The UI SHALL display the data sources used to generate the charity's evaluation to establish immediate transparency, including temporal bounding.

#### Scenario: Displaying the Financial Year
- **WHEN** rendering a charity's profile page and Impact Pathway
- **THEN** the UI MUST explicitly display the `financial_year` associated with the extracted data to ensure users understand the temporal snapshot of the financial metrics.
