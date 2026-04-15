## Why
Testing the v1 IES engine against unstructured, real-world charity reports revealed several critical epistemological and architectural misalignments. Specifically:
1. The IES aggregates both cumulative and annual metrics, alongside overlapping programmatic claims, leading to inflated outcome pools inconsistent with demographic beneficiary data.
2. The strict application of the evidence factor ($D_{evidence}$) obscures the charity's claimed impact, appearing overly punitive without UI context.
3. Species fallback heuristics are hardcoded in the Python service rather than residing in the PocketBase reference schema.
4. LLM extraction currently suffers from brittleness and hallucinations: exact-substring matching drops valid metrics, secondary intervention tags artificially inflate leverage multipliers, human-facing education triggers false `multi_domain_operations`, and the LLM occasionally misclassifies financial values or "potential" capacity as biological outcomes, whilst missing non-standard biological units like egg counts.

## What Changes
- **Data Schemas:** Expand `ref_moral_weights` to include generic baselines. Update `impact.schema.json` to handle primary intervention designation to prevent leverage inflation. Expand `analytics.schema.json` to return both a `claimed_ies` and an `evaluated_ies`.
- **Extraction Prompts (`n8n`):** Introduce strict positive and negative constraints to the `impact.system.md` to prevent financial/potential-impact hallucinations, mandate egg count inclusion, and properly bound `multi_domain_operations`.
- **Audit Engine (`utils_api`):** Refactor `calculate_ies` to filter for `annual` metrics, apply a bounding cap against total unique beneficiaries, use fuzzy matching for metric-to-event attribution, and query PocketBase for dynamic species fallbacks.
- **Frontend UI (`web`):** Update the IES Scorecard to prominently display the "Claimed Impact" alongside an "Epistemic Confidence Rating" (the $D_{evidence}$ discount applied).

## Impact
- **Affected specs:** `architecture`, `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** - `schemas/v1/impact_interventions.schema.json`
  - `schemas/v1/analytics.schema.json`
  - `n8n/prompt-templates/impact.system.md`
  - `utils_api/app/audits/impact.py`
  - `utils_api/app/schemas/analytics.py`
  - `web/layouts/partials/ies-scorecard.html`