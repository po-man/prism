## MODIFIED Requirements

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons and accurate mathematical scaling.

#### Scenario: Preserving Raw Integers with Table Multipliers
- **WHEN** validating the `financials.schema.json`
- **THEN** any object representing a financial figure (e.g., items within `income`, `expenditure`, `reserves`) MUST include a `scale_multiplier` property.
- **AND** the `scale_multiplier` MUST be an integer constrained to a strict enum: `[1, 1000, 1000000]`.
- **AND** the default value of `scale_multiplier` MUST be `1`.
- **AND** the primary `value` property MUST continue to store the raw integer exactly as it appears in the tabular source data.