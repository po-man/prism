## ADDED Requirements

### Requirement: Dynamic Extraction Schema Transformation
The system SHALL define a deterministic build process to transform canonical validation schemas into LLM-optimised extraction schemas by flattening enums, pruning downstream computational fields, and shortening high-token property names whilst preserving semantic context.

#### Scenario: Flattening Enums to Strings
- **WHEN** the build script encounters an `enum` array in the validation schema (e.g., `evidence_quality` with values like `RCT/Meta-Analysis`, `Quasi-Experimental`, etc.)
- **THEN** it MUST remove the `enum` keyword and explicitly set the `"type"` to `"string"`.
- **AND** it MUST append the allowed values to the end of the existing `description` string in the format: `[ALLOWED VALUES: 'val1', 'val2', ...]`.

#### Scenario: Removing Downstream Fields
- **WHEN** the build script compiles the extraction schema
- **THEN** it MUST remove fields that are strictly populated by downstream programmatic processes and cannot be deduced by the LLM from source text.
- **AND** specifically, the `resolved_url` field (which contains the strict `"format": "uri"` constraint) MUST be pruned from the `source` object.
- **AND** the `source_index` and `search_result_index` fields MUST be retained, as they are populated by the LLM to establish citation linkages.

#### Scenario: Semantic Key Shortening via `x-extract-key`
- **WHEN** a canonical validation schema contains the custom keyword `x-extract-key` on a property (e.g., `"x-extract-key": "unintended_cons"` on the `unintended_consequences_reported` property)
- **THEN** the build script MUST replace the canonical property key with the value of `x-extract-key` in the resulting extraction schema.
- **AND** it MUST humanise the original canonical key name (e.g., "Unintended Consequences Reported") and prepend it to the field's `description` followed by a colon and a space, ensuring the LLM retains the exact semantic context of the abbreviated key.
- **AND** the build script MUST output a deterministic mapping artifact (e.g., `key_mapping.json`) linking the abbreviated keys back to their canonical counterparts.