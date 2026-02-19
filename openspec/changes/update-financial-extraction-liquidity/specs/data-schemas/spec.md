## MODIFIED Requirements

### Requirement: Financial Health Definitions
The schema SHALL enforce standard financial accounting definitions suitable for ratio analysis and provide component-level fallbacks to ensure data resilience.

#### Scenario: Liquidity Inputs
- **WHEN** extracting balance sheet data
- **THEN** the schema MUST require `monthly_operating_expenses`.
- **AND** the schema MUST accept either `net_current_assets` OR a combination of `current_assets` and `current_liabilities`.

#### Scenario: Grading Evidence Quality
- **WHEN** extracting impact data
- **THEN** the `evidence_quality` field MUST be an Enum restricted to:
  - `"RCT/Meta-Analysis"` (Gold standard)
  - `"Quasi-Experimental"` (Control groups used)
  - `"Pre-Post"` (Before/After comparison only)
  - `"Anecdotal"` (Stories/Testimonials only)
  - `"None"` (No data provided)