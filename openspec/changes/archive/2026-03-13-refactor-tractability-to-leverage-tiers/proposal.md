## Why
Currently, the system presents intervention tractability using academic terminology (e.g., "RCT/Meta-Analysis", "Quasi-Experimental"), which alienates retail donors and the general public. Furthermore, the audit logic summarises a charity's entire operational portfolio into a single, highest-attained tier, obscuring their day-to-day operations. Finally, the existing `intervention_type` enum is too narrow, leading to inaccurate AI extraction and an overuse of the "other" category. By transitioning to "Intervention Leverage Tiers" and expanding the taxonomy, we can maintain Effective Altruism rigour while making the UI highly intuitive and transparent.

## What Changes
- **Taxonomy Expansion:** Expand the `intervention_type` enum in the `impact.schema.json` to 13 specific animal advocacy interventions.
- **Prompt Update:** Update the LLM system prompt with strict semantic definitions for all 13 intervention types to ensure deterministic categorization.
- **Backend Refactoring:** Replace the `INTERVENTION_TRACTABILITY_MAP` with an `INTERVENTION_LEVERAGE_MAP` grouping interventions into Tier 1 (Systemic Change), Tier 2 (Preventative Scale), and Tier 3 (Direct Care). Update `check_intervention_tractability` to aggregate an entire "Intervention Portfolio" rather than just yielding the single highest score.
- **UI Overhaul:** Update the Master Directory to display intuitive visual text badges (Tier 1, Tier 2, Tier 3) instead of academic tiers, and update the ITN Scorecard to render a full, itemised portfolio of verified interventions complete with provenance deep-links.

## Impact
- Affected specs: `data-schemas`, `audit-workflows`, `ui`
- Affected code: `schemas/v1/impact.schema.json`, `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/constants.py`, `utils_api/app/audits/impact.py`, `utils_api/tests/test_audit_impact.py`, `web/layouts/index.html`, `web/layouts/partials/itn-scorecard.html`, `web/layouts/partials/index-how-to-read.html`