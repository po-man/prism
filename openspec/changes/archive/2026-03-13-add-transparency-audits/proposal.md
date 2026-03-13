## Why
Currently, PRISM only evaluates charities against baseline compliance and impact thresholds (Pass/Warn/Fail). However, true Effective Altruism evaluation highly values *epistemic humility* and radical transparency. Organisations that openly report on unintended/negative impacts or sensitive operational metrics (like euthanasia rates in shelters) demonstrate exceptional integrity. We need a way to reward these "Advanced Checks" without penalising the vast majority of charities that follow the industry norm of non-disclosure.

## What Changes
- Add a new "Transparency" category to the audit engine.
- Expand the audit `status` taxonomy to include `bonus`, `not_disclosed`, and `n_a`.
- Implement **Check: Negative/Unintended Impact Disclosure**, applying to all organisations.
- Implement **Check: Live Release Rate Transparency**, applying conditionally only to organisations engaged in direct animal rescue or veterinary care.
- Update Gemini prompt templates and JSON schemas to extract these specific transparency indicators with strict provenance.
- Update the Hugo frontend to render these new statuses with distinct visual language (e.g., purple for Bonus, grey for Not Disclosed).

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/impact.schema.json`, `schemas/v1/analytics.schema.json`, `utils_api/app/audits/transparency.py`, `utils_api/app/audits/registry.py`, `n8n/prompt-templates/impact.system.md`, `web/layouts/partials/audit-checklist.html`, `web/layouts/index.html`