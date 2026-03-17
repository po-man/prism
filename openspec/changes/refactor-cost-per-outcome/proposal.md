# Change: Refactor Cost per Outcome Calculation to Intervention-Specific Metrics

## Why
Currently, PRISM calculates a blended "Cost per Outcome" by dividing an organisation's total programme expenditure by its total quantified animal beneficiaries. This approach mathematically penalises charities performing deep, high-cost interventions (e.g., lifelong sanctuary care, complex veterinary surgeries) while artificially inflating the apparent cost-effectiveness of organisations performing shallow, high-volume interventions (e.g., mass rabies vaccinations). From an Effective Altruism perspective, blending these fundamentally different outcomes produces a misleading metric. We must disaggregate costs by specific intervention types to ensure donors are comparing equivalent activities across the sector.

## What Changes
- ****BREAKING** Schema Updates:** Modify `v1/impact.schema.json` to map quantitative metrics to a strict taxonomy of intervention types. Modify `v1/financials.schema.json` to allow granular extraction of programme expenses mapped to these same intervention categories, rather than relying solely on a single `program_services` lump sum.
- **LLM Extraction Alignment:** Update the Gemini prompt templates (`impact.system.md`, `financials.system.md`) to enforce extraction against these new granular taxonomies, strictly prohibiting the LLM from hallucinating cost allocations that are not explicitly detailed in the source financial reports.
- **Audit Engine Refactoring:** Overhaul `calculate_cost_per_outcome` in `utils_api/app/audits/impact.py`. The logic will shift from a single division calculation to an intervention-specific attribution model. It will calculate a unit cost *only* when programme expenses can be explicitly linked to a specific intervention's outputs, or when an organisation is so specialised that >90% of its outputs fall under a single intervention. If costs are blended across multiple major interventions, the calculation will gracefully abort and flag as LOW confidence to prevent misrepresentation.
- **Frontend Presentation Shift:** Update the Hugo templates (`web/layouts/index.html`, `web/layouts/partials/myth-buster.html`) to handle a sparse data matrix. Instead of a single "Cost per Outcome" column, the UI will display primary intervention badges (e.g., "Vaccination", "Rescue") and render the specific unit cost within or alongside the badge only if the data successfully passed the audit engine's confidence checks.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** - `schemas/v1/impact.schema.json`
  - `schemas/v1/financials.schema.json`
  - `n8n/prompt-templates/impact.system.md`
  - `n8n/prompt-templates/financials.system.md`
  - `utils_api/app/audits/impact.py`
  - `utils_api/app/schemas/analytics.py`
  - `web/layouts/index.html`
  - `web/layouts/partials/myth-buster.html`
  - `web/layouts/partials/index-how-to-read.html`