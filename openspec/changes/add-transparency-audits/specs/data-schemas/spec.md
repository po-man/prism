## MODIFIED Requirements

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations, and qualifying calculations with confidence metadata.

#### Scenario: Advanced Check Taxonomy
- **WHEN** validating the `analytics.schema.json`
- **THEN** the `category` enum MUST include `"Transparency"`.
- **AND** the `status` enum MUST support Advanced Checks by allowing `"bonus"`, `"not_disclosed"`, and `"n_a"`, alongside the existing `"pass"`, `"warning"`, and `"fail"`.

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Extracting Transparency Indicators
- **WHEN** validating the `impact.schema.json`
- **THEN** it MUST include a top-level `transparency_indicators` object.
- **AND** this object MUST contain `unintended_consequences_reported` and `euthanasia_statistics_reported`.
- **AND** both properties MUST be objects containing a `value` (boolean) and a strictly validated `source` object to guarantee the provenance of the disclosure.