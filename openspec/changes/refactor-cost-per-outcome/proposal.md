## Why
[cite_start]Currently, PRISM's `cost_per_outcome` calculation divides total programme expenditure by a lumped sum of all animal beneficiaries across all programmes[cite: 1952, 1953]. This creates mathematically distorted and practically unusable metrics for multi-domain charities, as it treats a high-volume, low-cost intervention (e.g., vaccination) identically to a high-cost, low-volume intervention (e.g., complex wildlife rescue). [cite_start]To provide genuine value to asset owners and allocators making decisions based on EA principles[cite: 2581, 2582], we must replace this with an architecture that supports Activity-Based Costing and Pure-Play Cohort benchmarking.

## What Changes
- **Data Schemas (`impact` & `financials`):** - Refactor `explicit_unit_cost` from a single object into an array of `explicit_unit_costs`, enabling the LLM to extract multiple stated costs mapped directly to specific `InterventionTypeEnum` values.
  - Introduce a `program_breakdowns` array into the `financials.expenditure` schema to capture line-item programmatic spending.
- **Extraction Prompts:** Update the n8n prompt templates to instruct the LLM to actively hunt for intervention-specific funding appeals and granular programmatic financial breakdowns.
- **Audit Engine (`utils_api`):** Overhaul the `calculate_cost_per_outcome` function to:
  1. Calculate high-confidence costs directly from the new `explicit_unit_costs` array.
  2. Identify "Pure-Play" cohorts (where >80% of programmatic spend is dedicated to a single intervention) to safely calculate intervention-specific costs.
  3. Attempt to match granular `program_breakdowns` to specific `significant_events`.
- **Frontend UI (`web`):** Update the "Value for Money" scorecard to display an array of intervention-specific costs rather than a single, potentially misleading organisational average.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/*`, `n8n/prompt-templates/*`, `utils_api/app/audits/impact.py`, `utils_api/tests/*`, `web/layouts/partials/myth-buster.html`