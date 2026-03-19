# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Extracting Multiple Explicit Unit Costs
- **WHEN** validating the `context` object within `impact.schema.json`
- **THEN** the schema MUST define `explicit_unit_costs` as an array of objects, rather than a single object.
- **AND** each object in the array MUST contain an `intervention_type` field referencing the `InterventionTypeEnum` to link the cost to a specific EA cause area.
- **AND** each object MUST retain the `amount`, `currency`, `description`, and `source` fields to ensure strict provenance.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons and granular data provenance.

#### Scenario: Extracting Programmatic Financial Breakdowns
- **WHEN** validating the `expenditure` object within `financials.schema.json`
- **THEN** the schema MUST include a `program_breakdowns` array.
- **AND** this array MUST accept objects containing `programme_name` (string) and `amount` (referencing the `financial_figure` definition).
- **AND** this allows the system to capture granular line-item spending (e.g., "Mobile Spay Clinic Operations: $50,000") beyond the aggregated `program_services` total.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations, and qualifying calculations with confidence metadata.

#### Scenario: Advanced Check Taxonomy
- **WHEN** validating the `analytics.schema.json`
- **THEN** the `category` enum MUST include `"Transparency"`.
- **AND** the `status` enum MUST support Advanced Checks by allowing `"bonus"`, `"not_disclosed"`, and `"n_a"`, alongside the existing `"pass"`, `"warning"`, and `"fail"`.

### Requirement: Charity Metadata Schema
The system SHALL define a canonical JSON schema for extracting core identifying metadata applicable to charities worldwide, rather than restricted to a single jurisdiction.

#### Scenario: Pan-Asian Charity Extraction
- **WHEN** validating the metadata of an international charity
- **THEN** the schema MUST support a generalized `registration_id` field (replacing the HK-specific `s88_id`) to capture official non-profit identifiers globally.

### Requirement: Unified Provenance Schema Object
The system SHALL define a canonical `source` object to standardize data provenance tracking across all domains, completely replacing unstructured citation strings and fragmented URL/quote fields.

#### Scenario: Enforcing the Unified Source Structure
- **WHEN** any extraction schema (`impact.schema.json` or `financials.schema.json`) requires provenance tracking
- **THEN** it MUST embed the following `source` object structure:
  ```json
  {
    "type": "object",
    "properties": {
      "source_type": { 
        "type": "string", 
        "enum": ["annual_report", "financial_report", "web_search"] 
      },
      "page_number": { 
        "type": ["integer", "null"],
        "description": "1-based absolute PDF page index."
      },
      "search_result_index": { 
        "type": ["integer", "null"],
        "description": "0-based index of the search result array."
      },
      "quote": { 
        "type": ["string", "null"],
        "description": "Exact, verbatim text extracted from the source."
      },
      "resolved_url": { 
        "type": ["string", "null"], 
        "format": "uri",
        "description": "Computed deep-link URL (populated by the Utils API)."
      }
    },
    "required": ["source_type", "page_number", "search_result_index", "quote", "resolved_url"]
  }
  ```

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

