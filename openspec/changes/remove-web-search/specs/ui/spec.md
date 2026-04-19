## MODIFIED Requirements

### Requirement: Data Provenance Indicators
The UI SHALL display the data sources used to generate the charity's evaluation to establish immediate transparency, including temporal bounding, strictly limited to formal documentation.

#### Scenario: Displaying the Financial Year and Attached Reports
- **WHEN** rendering a charity's profile page and Impact Pathway
- **THEN** the UI MUST explicitly display the `financial_year` associated with the extracted data.
- **AND** it MUST ONLY display provenance icons for the "Annual Report" and "Financial Report".
- **AND** it MUST NOT render any visual indicators or icons suggesting web searches were performed.

### Requirement: Master Comparative Table (Landing Page)
The UI SHALL provide a high-level, sortable directory of all audited charities to facilitate rapid EA-aligned comparative analysis, displaying metric confidence visually.

#### Scenario: Comparing ITN and Financial Metrics
- **WHEN** a user visits the root `/` directory (Landing Page)
- **THEN** the "Data Sources" column in the Master Table MUST display icons exclusively for "Annual Report" and "Financial Report", greying out missing sources.
- **AND** the column's sorting logic MUST calculate the score out of a maximum of 2 sources (Annual and Financial).

### Requirement: Interactive Provenance Badges
The UI SHALL render explicit, interactive citation badges for all quantitative figures and claims to facilitate immediate human verification against source documents.

#### Scenario: Rendering Document Citations
- **WHEN** the Hugo template iterates over `beneficiaries`, `metrics`, `significant_events`, or `financials` that contain a populated `source` object
- **THEN** it MUST render a small UI badge adjacent to the claim (e.g., an icon with "📄 p. 12" for PDFs).
- **AND** it MUST NOT check for or render web search specific formatting or icons.