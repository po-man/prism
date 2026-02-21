# Change: Enhance Audit Checklist with EA Impact Metrics

## Why
Currently, the `utils_api` evaluates charities primarily on regulatory compliance and financial health (e.g., reserve caps, liquidity, remuneration disclosure). While critical, these checks do not measure a charity's actual effectiveness. To align with Effective Altruism (EA) principles, the system needs to programmatically assess how well a charity understands its impact. By introducing programmatic checks for Evidence Quality, Counterfactual Awareness, Cost-per-Outcome, and Funding Neglectedness, we can generate a data-driven "Impact Awareness" profile for every NGO.

## What Changes
- **Audit Logic Expansion:** Create a new `impact.py` audit module in the validation service (`utils_api`) containing four new checks:
  - `check_evidence_quality`: Evaluates if the charity relies on high-quality evidence (e.g., RCTs) versus anecdotal claims.
  - `check_counterfactual_baseline`: Verifies if the charity tracks what would happen in the absence of their intervention.
  - `check_cost_per_outcome`: A purely informational calculation combining `program_services` expenses with the primary outcome's `population` or `quantitative_data.value`.
  - `check_funding_neglectedness`: Calculates the ratio of government subvention to total income to flag highly-funded versus neglected interventions.
- **Prompt Refinement:** Update the n8n prompt templates for the Impact Agent to instruct the LLM to output concise, UI-friendly strings for `severity_dimensions` and `counterfactual_baseline`, avoiding long paragraphs that break frontend layouts.

## Impact
- **Affected specs:** `audit-workflows`, `data-schemas`
- **Affected code:** - `utils_api/app/audits/impact.py` (New)
  - `utils_api/app/audits/registry.py`
  - `n8n/prompt-templates/impact.system.md`
  - `n8n/prompt-templates/impact.user.md`