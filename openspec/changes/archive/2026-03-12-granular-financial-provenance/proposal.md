## Why
Following the successful unification of the `source` object schema and resolution endpoint, we identified a critical limitation in how financial data provenance is tracked. Currently, the `financials.schema.json` utilises a single top-level `sources` array. This structure forces analysts to rely on general citations for the entire financial entity, making it difficult to verify individual figures (e.g., distinguishing the source of `program_services` expenditure versus `government_grants` income, which often reside on different pages or notes within an Annual Financial Report). To maintain strict Effective Altruism standards of transparency and verifiability, every single extracted financial figure must bear its own exact citation and deep-link.

## What Changes
1.  **Granular Schema Definitions:** We will introduce a new `financial_figure` definition in `financials.schema.json` that encapsulates both a `value` (number) and an optional `source` object. All properties within `income`, `expenditure`, `reserves`, `lsg_specifics`, and `ratio_inputs` will be refactored to use this new definition.
2.  **Prompt Engineering:** The `financials.system.md` prompt template will be updated to instruct the LLM to map a precise `source` object (including absolute page index and verbatim quote) to each individual financial figure, rather than aggregating them in a top-level array.
3.  **Orchestrator Resolution Logic:** The `Resolve Provenance (Financials)` n8n node will be updated to pass the entire `financials` data object to the `utils_api` `/resolve-provenance` endpoint. Because the Python resolution logic is recursive, it will automatically seek out and resolve all deeply nested `source` objects without requiring backend code changes.
4.  **Audit Engine Refactoring:** The deterministic audit functions in `utils_api/app/audits/` (e.g., `check_liquidity`, `check_reserve_cap`, `calculate_cost_per_outcome`) will be updated to access `.value` when performing calculations.
5.  **UI Enhancements:** Hugo templates (`impact-pathway.html` and `myth-buster.html`) will be updated to render the `provenance-badge.html` partial directly adjacent to specific financial figures, ensuring line-item transparency on the static site.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** - `schemas/v1/financials.schema.json`
  - `n8n/prompt-templates/financials.system.md`
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`
  - `utils_api/app/audits/financial.py`
  - `utils_api/app/audits/impact.py`
  - `utils_api/tests/*`
  - `web/layouts/partials/impact-pathway.html`
  - `web/layouts/partials/myth-buster.html`