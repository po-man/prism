# Change: Refactor Quantitative Impact Focus and IES Logic

## Why
The current PRISM UI includes an "Impact Pathway" that surfaces qualitative activities and outcomes. This creates cognitive overload for donors and distracts from the core quantitative Effective Altruism metrics. Furthermore, the `utils_api` relies on brittle fuzzy-matching to link metrics to interventions and species for the Impact Equivalency Score (IES). We can achieve a much more robust, deterministic outcome by injecting the exact PocketBase reference keys (Species, Intervention, Evidence) directly into the LLM schema at runtime, forcing the model to explicitly map each metric. Finally, self-reported evidence tiers (None, Anecdotal, Pre-Post) are functionally indistinguishable in the context of charity annual reports and must be merged to simplify the epistemic discount model.

## What Changes
1. **Schema & Database Pruning:** - Remove the `human` moral weight from PocketBase. 
   - Merge `None`, `Anecdotal`, and `Pre-Post` into a single `Self-Reported` evidence tier in PocketBase and the metrics schema.
   - Delete the `significant_events` array from the `impact_interventions` schema entirely.
2. **Dynamic Schema Injection:** Update the n8n orchestration pipeline to fetch the exact `species_key`, `intervention_key`, and `evidence_key` values from the PocketBase reference collections at runtime. These will be dynamically injected as `enum` constraints into the `impact_metrics` JSON schema before it is passed to Gemini.
3. **Audit Engine Simplification:** Refactor the `calculate_ies` function in `utils_api` to strip out all fuzzy string matching. The engine will now calculate the IES by directly looking up the keys explicitly assigned to each metric by the LLM.
4. **UI Streamlining:** Completely remove the `impact-pathway.html` component. The "Inputs" (financial expenditure) will be migrated to the "Value for Money" section, and the "Counterfactual Baseline" will be migrated to the "Impact Profile" section.

## Impact
- **Affected specs:** `ui`, `data-schemas`, `audit-workflows`
- **Affected code:** - `pocketbase/migrations/*`
  - `schemas/v1/impact_metrics.schema.json`
  - `schemas/v1/impact_interventions.schema.json`
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`
  - `utils_api/app/audits/impact.py`
  - `web/layouts/partials/impact-pathway.html` (deleted)
  - `web/layouts/partials/itn-scorecard.html`
  - `web/layouts/partials/myth-buster.html`
  - `web/layouts/_default/single.html`