# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, strictly enforcing the extraction of verbatim evidence and explicitly mapping metrics to global reference keys.

#### Scenario: Strict Metric Classification Keys
- **WHEN** validating the `impact_metrics.schema.json`
- **THEN** each metric MUST require a `species_key` and an `intervention_key` (both strings).
- **AND** these fields MUST conform to the exact enums injected dynamically by the orchestrator at runtime.

#### Scenario: Merging Self-Reported Evidence Types
- **WHEN** validating the `evidence_quality` of a metric
- **THEN** the allowed enum values MUST strictly be `["RCT/Meta-Analysis", "Quasi-Experimental", "Self-Reported"]`.
- **AND** any legacy unstructured or anecdotal evidence MUST be classified exclusively under `Self-Reported`.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons and accurate mathematical scaling.

#### Scenario: Preserving Raw Integers with Table Multipliers
- **WHEN** validating the `financials.schema.json`
- **THEN** any object representing a financial figure (e.g., items within `income`, `expenditure`, `reserves`) MUST include a `scale_multiplier` property.
- **AND** the `scale_multiplier` MUST be an integer constrained to a strict enum: `[1, 1000, 1000000]`.
- **AND** the default value of `scale_multiplier` MUST be `1`.
- **AND** the primary `value` property MUST continue to store the raw integer exactly as it appears in the tabular source data.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items and calculated metrics specific to Effective Altruism principles, supporting detailed elaborations and explicitly storing the data lineage used for evaluation.

#### Scenario: Propagating Metric Provenance to IES Breakdown
- **WHEN** validating the `analytics.schema.json` for the `impact_equivalency_score` metric
- **THEN** the items within the `details.breakdown` array MUST include an optional `source` object.
- **AND** this `source` object MUST support the standard provenance fields (`source_type`, `page_number`, `quote`, `resolved_url`) to enable the frontend to trace the high-level impact claim back to its origin.

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
        "enum": ["attached_report"] 
      },
      "source_index": {
        "type": ["integer", "null"],
        "description": "0-based index of the attached document."
      },
      "page_number": { 
        "type": ["integer", "null"],
        "description": "1-based absolute PDF page index."
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
    "required": ["source_type", "quote", "resolved_url"]
  }
  ```
- **AND** it MUST NOT include `web_search` in the `source_type` enum or support a `search_result_index` field.

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

### Requirement: Reference Data Collections for IES Constants
The system SHALL define static reference collections in PocketBase to store philosophical and epistemic constants, ensuring they are decoupled from individual charity records and can be updated globally.

#### Scenario: Pruning Out-of-Scope Moral Weights
- **WHEN** the `ref_moral_weights` collection is queried
- **THEN** it MUST NOT contain a `human` species key, enforcing the platform's strict focus on animal advocacy.

#### Scenario: Normalising Epistemic Discounts
- **WHEN** the `ref_evidence_discounts` collection is queried
- **THEN** it MUST return a single `Self-Reported` category with a unified penalty multiplier, eliminating the artificial distinction between `Pre-Post`, `Anecdotal`, and `None` for self-published charity reports.

