# openspec/changes/add-donor-transparency-ui/proposal.md

# Change: Add Donor Transparency & EA Translation UI

## Why
Currently, the PRISM report cards present analytical data, but they lack immediate visual cues that retail donors rely on to make quick, informed decisions. To bridge the gap between rigorous Effective Altruism (EA) evaluation and donor psychology, the interface must immediately communicate three things: 
1. **Data Provenance:** Can this charity be trusted, or is it a black box? 
2. **Target Species:** Does this charity operate in a highly neglected area (e.g., farmed/wild animals) or a saturated one (companion animals)?
3. **Tangible Tractability:** What does a standard donation actually achieve in the real world?

## What Changes
- **Source Provenance Indicators:** Introduce a visual icon array at the top of the charity profile denoting the presence or absence of core documents (Annual Report, Audited Financials) and Web Intelligence. Missing documents will be visually disabled.
- **Animal Beneficiary Badges:** Map the existing `beneficiary_type` data to prominent species icons (e.g., dogs/cats vs. chickens/pigs) to visually reinforce the EA "Neglectedness" metric.
- **Retail Impact Translator:** Modify the existing Python audit engine (`utils_api`) to automatically calculate and return a "Retail Donor Equivalent" (e.g., "What a $1,000 donation achieves") derived from the `check_cost_per_outcome` calculation, and display this prominently in the Value for Money UI.

## Impact
- **Affected specs:** `ui`, `audit-workflows`
- **Affected code:** `utils_api/app/audits/impact.py`, `web/layouts/_default/single.html`, `web/layouts/partials/itn-scorecard.html`, `web/layouts/partials/myth-buster.html`