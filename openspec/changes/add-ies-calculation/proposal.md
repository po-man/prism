## Why
Currently, PRISM extracts raw impact metrics but lacks a unified, cross-species, and cross-intervention scoring mechanism to compare charities. To adhere to Effective Altruism principles, we must implement an Impact Equivalency Score (IES) that mathematically standardises outcomes using moral weights, evidence discounts, and probabilistic leverage multipliers.

## What Changes
- **PocketBase Reference Data:** Introduce new collections (`ref_moral_weights`, `ref_evidence_discounts`, `ref_intervention_baselines`) to store hardcoded philosophical and epistemic constants.
- **Data Schemas:** Expand the extraction schemas to explicitly capture `species`, `intervention_typology`, and `evidence_claim`. Expand the analytics schema to store the computed IES breakdown.
- **Logic Layer (`utils_api`):** Implement the IES calculation engine. The API will dynamically fetch PocketBase constants, query external macroeconomic/agricultural APIs (e.g., FAOSTAT, World Bank) for addressable populations and PPP adjustments, and execute the BOTEC (Back-of-the-Envelope Calculation) for systemic leverage.
- **Frontend (Hugo):** Add a self-explanatory IES breakdown card to the charity profile page to transparently display how the score was calculated.

## Impact
- Affected specs: `data-schemas`, `architecture`, `audit-workflows`, `ui`
- Affected code: `pocketbase/migrations/*`, `utils_api/app/audits/impact.py`, `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`, `web/layouts/partials/*`