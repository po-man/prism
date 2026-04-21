# Change: Remove M&E Check, Enhance Counterfactual Provenance, and Expose Audit Criteria

## Why
To maintain PRISM's integrity as a deterministic Effective Altruism (EA) evaluation engine, we must minimise subjective scoring and maximise verifiable provenance. The `Check Monitoring and Evaluation` item evaluates self-reported evidence tiers, which introduces subjectivity and overlaps with the stricter `Evidence Quality` tractability metric. Furthermore, our current counterfactual baselines lack direct citations, relying on LLM-synthesised descriptions. Finally, hiding the Pass/Warn/Fail threshold logic within frontend HTML tooltips obscures the EA rationale from the end-user, limiting the platform's educational value.

## What Changes
1. **Deprecation:** Completely remove the `Check Monitoring and Evaluation` from the pipeline, the Python Audit Engine, and all associated tests.
2. **Schema Extension (Data Vault):** Introduce a `source` object (containing `url` and `quote`) to the `counterfactual_baseline` in `schemas/v1/impact_metrics.schema.json`. Deprecate the synthesised `description` field. Add a `criteria` string to the `Details` object in `schemas/v1/analytics.schema.json` to store static threshold rules.
3. **Prompt Engineering:** Update the `impact.system.md` prompt to enforce the extraction of exact, verbatim text into the new `source.quote` field when justifying the counterfactual baseline.
4. **Audit Logic (Python Engine):** Update the `utils_api` to inject plain-text evaluation rules into the new `criteria` field for *every* audit check. Update the counterfactual check to pass the `source.quote` into the checklist's `elaboration` field.
5. **UI Architecture (Hugo):** - **Impact Pathway:** Replace the synthesised counterfactual description with the verbatim quote and render a hyperlinked provenance badge.
    - **Audit Checklist:** Refactor the `<details>` dropdown to cleanly separate the logic into a top section ("Evaluation Criteria") and a bottom section ("Result & Evidence").

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/impact_metrics.schema.json`, `schemas/v1/analytics.schema.json`, `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/registry.py`, `utils_api/app/audits/impact.py`, `web/layouts/partials/impact-pathway.html`, `web/layouts/partials/audit-checklist.html`