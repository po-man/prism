# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles in animal advocacy.

#### Scenario: Cause Area Neglectedness Check
- **WHEN** the audit engine generates the `check_items` array
- **THEN** it MUST include an item with ID `check_cause_area_neglectedness` that evaluates the tractability and neglectedness of the target species.

