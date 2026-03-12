## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Impact Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting charity impact data, including proportional beneficiary breakdowns, exact evidence citations, temporal bounding, and granular intervention classification.

#### Scenario: Embedding Unified Provenance in Impact Data
- **WHEN** validating the `impact.schema.json`
- **THEN** the items within the `metrics`, `significant_events`, and `beneficiaries` arrays MUST embed the unified `source` object.
- **AND** the legacy fields `source_citation`, `source_url`, `source_document`, `evidence_quote`, `source_quote`, and `search_result_index` MUST be entirely removed from the root properties of these items.

### Requirement: Financials Schema Definition
The system SHALL define a canonical JSON schema for extracting and persisting financial data, strictly preserving original values while enabling standardized multi-currency comparisons.

#### Scenario: Adding Provenance to Financial Data
- **WHEN** the `financials.schema.json` is validated
- **THEN** the root of the schema MUST include a `sources` array.
- **AND** the items in this array MUST adhere to the unified `source` object definition, allowing the LLM to cite the primary pages (e.g., Statement of Financial Position, Income Statement) used to extract the financial figures.