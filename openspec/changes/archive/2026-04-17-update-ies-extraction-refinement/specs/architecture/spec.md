## MODIFIED Requirements

### Requirement: Separation of Concerns
The architecture SHALL strictly decouple orchestration, intelligence extraction, data validation, and frontend rendering.

#### Scenario: Generic Species Fallback Decoupling
- **WHEN** the `utils_api` calculates the Impact Equivalency Score (IES) and encounters an unmapped species
- **THEN** it MUST NOT rely on hardcoded Python dictionaries to resolve the fallback.
- **AND** it MUST query the `ref_moral_weights` reference collection in PocketBase for generic baseline records (e.g., `generic_companion`, `generic_farmed`, `generic_wild`, `generic_unspecified`) based on the charity's dominant beneficiary domain.