## ADDED Requirements

### Requirement: Dynamic BOTEC and External Data Resolution
The `utils_api` microservice SHALL act as the central computational engine for Expected Value (EV) and IES generation, bridging extracted JSON data with external macro-datasets.

#### Scenario: Querying External APIs for Systemic Scale and PPP
- **WHEN** the `utils_api` evaluates a systemic intervention (e.g., a national policy change) where the raw extracted scale is undefined or represents a geographic region
- **THEN** it MUST dynamically query an external agricultural database (e.g., FAOSTAT) to determine the Total Addressable Population.
- **AND** it MUST query a macroeconomic database (e.g., World Bank API) to apply Purchasing Power Parity (PPP) adjustments to the extracted financial expenditure, ensuring standardised cost-effectiveness comparisons.