# Change: Refactor System for EA-Aligned Animal Advocacy

## Why
The current system is hardcoded to evaluate generalized Hong Kong charities, primarily those receiving Social Welfare Department (SWD) subventions. It looks for human-centric metrics (e.g., QALYs, student grades) and SWD-specific financial structures. Furthermore, the existing workflow assumes a rigid set of documents (Annual Reports, Financial Reports, Remuneration Reports). To fulfill the PRISM mandate, we must pivot the architecture to evaluate animal advocacy organizations through an Effective Altruism (EA) lens. This requires:
1. Prioritizing neglected cause areas (e.g., farmed and wild animals over companion animals).
2. Deprecating the governance evaluation layer, as formal governance/remuneration reports are rarely applicable or available for grassroots animal rescues.
3. Enhancing the pipeline to dynamically handle varying levels of data completeness (graceful degradation when specific reports are missing).

## What Changes
- **Data Ingestion & Orchestration:** Deprecate the n8n SWD AFR web scraper. Replace it with a robust ingestion workflow that reads from a managed registry of HK animal charities. The workflow will use conditional routing to gracefully bypass missing documents (e.g., evaluating Impact even if Financials are unavailable).
- **Deprecations:** Completely remove the `governance` JSON schema, the `governance` prompt templates, the `check_remuneration` audit logic, and the corresponding n8n extraction branches.
- **Schemas:** Refactor `impact.schema.json` to categorize animal beneficiary types (companion, farmed, wild) and intervention types (direct rescue, corporate outreach, policy advocacy).
- **Prompt Engineering:** Rewrite `impact.system.md` and `impact.user.md` to instruct the Gemini 2.5 model to extract animal-centric impact metrics and counterfactuals.
- **Audit Logic (`utils_api`):** Add `check_cause_area_neglectedness` to automatically flag/reward organizations working in highly neglected areas (farmed/wild animals) vs. saturated areas. Soften the `check_reserve_cap` to look at general reserve ratios.
- **UI/UX:** Update the Hugo `itn-scorecard.html` to clearly visualize EA neglectedness and remove governance checklist items.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `n8n/workflows/*.json`, `n8n/prompt-templates/*.md`, `schemas/v1/*.json`, `utils_api/app/audits/*.py`, `web/layouts/partials/*.html`