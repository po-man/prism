## ADDED Requirements

### Requirement: Analytics Check-Item Schema
The system SHALL define the allowed categories for the audit checklist results to accommodate transparency reporting.

#### Scenario: Extending the Category Enum
- **WHEN** validating an `analytics` object
- **THEN** the `category` property of a `checkItem` MUST accept "Data Transparency" as a valid enum, in addition to "Financial Health", "Governance", "Impact Awareness", and "Risk Management".