# audit-workflows Specification (Delta)

## MODIFIED Requirements
### Requirement: Idempotent Execution & State Persistence
The system SHALL employ a checkpointing strategy to ensure that high-cost operations are not repeated unnecessarily.

#### Scenario: Analytical Re-run
- **WHEN** raw data (financials/governance) exists in PocketBase
- **AND** only the audit logic in `utils_api` has changed
- **THEN** the system MUST be able to re-run the analytics phase without re-extracting data from PDFs.

## ADDED Requirements
### Requirement: Binary Audit Computation
The system MUST compute a series of pass/fail check-items based on extracted statutory and financial data.

#### Scenario: Reserve Cap Validation
- **GIVEN** an NGO has a cumulative LSG reserve of $1M and operating expenses of $3M
- **WHEN** the audit logic calculates the ratio (0.33)
- **THEN** the `check_reserve_cap` item MUST return `status: "fail"`
- **AND** include the calculation details in the `details` field.