## Why
Currently, the LLM extraction pipeline occasionally misinterprets the definition of a "beneficiary" by counting animal products (e.g., eggs) as individual animals, or by extracting projected/potential impact numbers instead of actualised, historical outcomes. Furthermore, the `impact.schema.json` restricts beneficiary types to a strict enum of `companion_animals`, `farmed_animals`, and `wild_animals`. This forces the LLM to guess the classification when source documents ambiguously refer to "other animals", leading to inaccurate neglectedness calculations. 

## What Changes
1. **Schema Extension:** Introduce an `unspecified` value to the `beneficiary_type` enum within `impact.schema.json` to handle ambiguous classifications safely.
2. **Prompt Engineering:** Update the `impact.system.md` system prompt to strictly define what constitutes an animal (excluding products like eggs/meals), enforce the extraction of only *actualised* impact (excluding potential/guesses), and provide clear context rules for species classification (e.g., stray dogs are still `companion_animals`).
3. **UI Logic:** Update the Hugo templates (`index.html` and `itn-scorecard.html`) to safely ingest the `unspecified` category. In the master directory, this category will remain hidden to preserve the visual focus on EA cause areas. On individual organisation pages, the `unspecified` category will only render if its population is greater than zero.
4. **Audit Logic:** Update the `check_cause_area_neglectedness` function in `utils_api/app/audits/impact.py` to incorporate the new `unspecified` type in the baseline population map, ensuring it does not artificially inflate the high-neglectedness ratio.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/impact.schema.json`, `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/impact.py`, `web/layouts/index.html`, `web/layouts/partials/itn-scorecard.html`