# openspec/changes/replace-risk-with-web-impact/specs/data-schemas/spec.md

## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns and exact evidence citations.

#### Scenario: Web-Sourced Data Provenance
- **WHEN** validating the impact data of an animal charity
- **THEN** the `metrics` array items MUST include an optional `source_url` (string) field to capture the specific web URL if the metric was extracted from a web snippet.
- **AND** the `significant_events` array items MUST include an optional `source_url` (string) field for the same provenance tracking purpose.

## REMOVED Requirements

### Requirement: Charity Risk Assessment Schema
**Reason**: The risk assessment capability is being deprecated to allocate computational resources and focus entirely on EA Impact Alignment. 
**Migration**: Delete `schemas/v1/risk.schema.json` and remove the `risk` property from the `OrganisationRecord` Pydantic model.