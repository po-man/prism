## Why
Currently, PRISM equates Effective Altruism's "Tractability" with the quality of evidence a charity provides in its own reports (e.g., RCTs vs. anecdotal claims). This creates a critical epistemological flaw: it conflates **Intervention-Level Tractability** (is the method scientifically proven generally?) with **Organisation-Level Monitoring & Evaluation** (does this specific charity measure their own impact rigorously?). A highly effective grassroots charity executing a highly tractable intervention (e.g., a corporate welfare campaign) would incorrectly receive a low Tractability score simply because they lack the budget to conduct independent RCTs. We must decouple these two concepts to align with true EA methodology while improving LLM classification accuracy.

## What Changes
1. **Schema Expansion:** Convert `intervention_type` in `impact.schema.json` from a string to an array of strings to support multi-label classification. Expand the taxonomy to cover the full "fat tail" of animal advocacy interventions, and add an `intervention_type_other_description` field to catch edge cases.
2. **Prompt Engineering:** Inject a semantic definition rubric directly into the Gemini extraction prompts so the LLM understands exactly what constitutes each intervention category, maximising the "hit rate".
3. **Audit Engine Logic:** - Introduce an `INTERVENTION_TRACTABILITY_MAP` registry within the `utils_api` to serve as the ground-truth EA evidence base.
   - Add a new `check_intervention_tractability` function that evaluates the highest proven intervention a charity engages in.
   - Rename the existing `check_evidence_quality` function to `check_monitoring_and_evaluation` to accurately reflect its purpose (evaluating self-reported evidence).
4. **UI Update:** Refactor the "Tractability" card on the ITN Scorecard to display the general EA tractability basis derived from the new audit check, rather than the charity's self-reported evidence quote.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/impact.schema.json`, `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/registry.py`, `utils_api/app/audits/impact.py`, `web/layouts/partials/itn-scorecard.html`