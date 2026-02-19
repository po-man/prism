## MODIFIED Requirements

### Requirement: Binary Audit Computation
The system MUST compute a series of pass/fail check-items based on extracted statutory and financial data. The system MUST employ fallback calculations if aggregate metrics are missing but component metrics are present.

#### Scenario: Reserve Cap Validation
- **GIVEN** an NGO has a cumulative LSG reserve of $1M and operating expenses of $3M
- **WHEN** the audit logic calculates the ratio (0.33)
- **THEN** the `check_reserve_cap` item MUST return `status: "fail"`
- **AND** include the calculation details in the `details` field.

#### Scenario: Liquidity Fallback Calculation
- **GIVEN** the extracted data lacks `net_current_assets`
- **BUT** the data contains `current_assets` of $5M and `current_liabilities` of $2M
- **WHEN** the audit logic evaluates liquidity
- **THEN** the system MUST dynamically calculate `net_current_assets` as $3M and proceed with the standard liquidity ratio computation.