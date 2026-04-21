## 1. Schema Refactoring (`schemas`)
- [x] 1.1 In `schemas/v1/analytics.schema.json`, locate `definitions.iesMetric.properties.details.properties.breakdown.items.properties`.
- [x] 1.2 Add a new `"source"` property that accepts an object or null, mimicking the standard provenance structure (containing `source_type`, `page_number`, `quote`, `resolved_url`).
- [x] 1.3 Run the extraction schema generation script: `python scripts/generate_extraction_schemas.py` to ensure build artifacts remain synchronized.

## 2. Python Audit Engine Updates (`utils_api`)
- [x] 2.1 In `utils_api/app/schemas/analytics.py`, update the `BreakdownItem` Pydantic model to include `source: dict | None = None` (or map it to a defined `Source` model if preferred).
- [x] 2.2 In `utils_api/app/audits/impact.py`, locate the `calculate_ies` function.
- [x] 2.3 Inside the `for metric in record.impact.metrics.metrics:` loop, update the `ies_breakdown.append(...)` dictionary.
- [x] 2.4 Add `"source": metric.source.model_dump(exclude_unset=True) if metric.source else None` to the appended dictionary.

## 3. UI / Hugo Refactoring (`web`)
- [x] 3.1 In `web/layouts/partials/ies-scorecard.html`, locate the `Impact Claim` column rendering: `<td class="p-3 font-medium text-gray-800 italic w-1/3">"{{ .metric_name }}"</td>`.
- [x] 3.2 Update the markup to wrap the metric name in an italicised span, and conditionally render the provenance badge adjacent to it:
  ```html
  <td class="p-3 font-medium text-gray-800 w-1/3">
    <span class="italic">"{{ .metric_name }}"</span>
    {{ with .source }}{{ partial "provenance-badge.html" . }}{{ end }}
  </td>
  ```