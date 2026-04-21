## Why
The Impact Equivalency Score (IES) Scorecard currently lists "Impact Claims" (the names of the metrics evaluated) but lacks direct, line-item provenance badges for the claims themselves. While we expose the empirical data sources in the "Outcome" hover states, providing a top-level provenance badge next to the claim's name reinforces immediate trust and allows users to jump directly to the source document where the metric was originally stated. 

## What Changes
1. **Schema Extension:** Update `schemas/v1/analytics.schema.json` to include a `source` object within the `iesMetric` breakdown items.
2. **Audit Engine Routing:** Update the `calculate_ies` function in the Python `utils_api` to map the `metric.source` object from the impact payload into the final IES breakdown dictionary.
3. **UI Standardisation:** Refactor the Hugo template `ies-scorecard.html` to conditionally render the `provenance-badge.html` partial next to the metric name.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/analytics.schema.json`, `utils_api/app/schemas/analytics.py`, `utils_api/app/audits/impact.py`, `web/layouts/partials/ies-scorecard.html`