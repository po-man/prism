## MODIFIED Requirements

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