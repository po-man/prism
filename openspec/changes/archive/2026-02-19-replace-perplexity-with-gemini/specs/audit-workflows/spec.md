# audit-workflows Specification (Delta)

## MODIFIED Requirements
### Requirement: Statutory Data Extraction (LSG Only)
The Extractor Agent SHALL identify compliance data points defined in the LSG Manual using multimodal document intelligence.

#### Scenario: LSG Reserve Calculation
- **WHEN** processing an LSG-subvented NGO's PDF report
- **THEN** the agent MUST use a multimodal LLM to ingest the raw PDF, parse the complex financial tables natively, and extract the `lsg_reserve_amount` and `operating_expenditure`.
- **AND** calculate if the reserve exceeds 25% of operating expenditure.

### Requirement: Hallucination Defense
The system SHALL NOT infer data that is not explicitly present in the text or verified through search grounding.

#### Scenario: Ambiguous Financials
- **WHEN** the document does not explicitly state "Program Expenses"
- **THEN** the agent MUST return `null`.

#### Scenario: Enforcing Output Structure
- **WHEN** generating data to be passed to the validation service
- **THEN** the system MUST use native API JSON schema enforcement rather than prompt-based coercion to eliminate structural hallucinations.

## ADDED Requirements
### Requirement: Grounded Risk Assessment
The Risk Agent SHALL evaluate the reputational and regulatory risks of charities by executing real-time web searches to gather external context.

#### Scenario: Identifying Recent Scandals
- **WHEN** assessing an NGO's risk profile
- **THEN** the system MUST leverage search-grounded AI to query the live web for recent controversies, scandals, or Audit Commission reports.
- **AND** if no negative news is found, explicitly state "None" in the summaries and set flags to false.