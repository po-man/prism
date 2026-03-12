# data-schemas Specification

## Purpose
This specification defines the data contracts for the entire system. It provides canonical JSON schemas for all data entities, including ingestion payloads, extracted financial and impact metrics, and the final `analytics` object. These schemas ensure data integrity and consistency as information moves from extraction to persistence and final presentation.
## Requirements
### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Embedding Unified Provenance in Impact Data
- **WHEN** validating the `impact.schema.json`
- **THEN** the items within the `metrics`, `significant_events`, and `beneficiaries` arrays MUST embed the unified `source` object.
- **AND** the legacy fields `source_citation`, `source_url`, `source_document`, `evidence_quote`, `source_quote`, and `search_result_index` MUST be entirely removed from the root properties of these items.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons and granular data provenance.

#### Scenario: Enforcing Figure-Level Provenance
- **WHEN** the `financials.schema.json` is validated
- **THEN** the root of the schema MUST NOT contain a top-level `sources` array.
- **AND** a new definition called `financial_figure` MUST be created, comprising a `value` (number or null) and a `source` (referencing the unified source object, or null).
- **AND** all individual metrics within the `income`, `expenditure`, `reserves`, `lsg_specifics`, and `ratio_inputs` objects MUST strictly adhere to the `financial_figure` definition, enabling line-item attribution.

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations, and qualifying calculations with confidence metadata.

#### Scenario: Tiering Calculated Metrics
- **WHEN** the `analytics.schema.json` is validated
- **THEN** items within `calculated_metrics` MUST include `confidence_tier` (enum: `["HIGH", "MEDIUM", "LOW"]`) and `confidence_note` (string).
- **AND** the `value` property MUST allow `null` to accommodate aborted calculations in Low Confidence scenarios.

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

