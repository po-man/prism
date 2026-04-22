## Why
The current PRISM UI presents a few inconsistencies and opportunities for visual optimisation. Firstly, the Expense Breakdown card entirely disappears when financial expenditure data is missing, which causes jarring layout shifts and inconsistency across charity profiles. Secondly, the Audit Summary on the master directory uses constant opacity for its pass/warning/fail indicators, which fails to visually communicate the *proportion* of performance. Lastly, charities with highly verified interventions can overwhelm the UI by rendering an excessive number of provenance badges in the Intervention Portfolio.

## What Changes
1.  **Expense Breakdown Fallback:** Modify the Value for Money component so that the "Expense Breakdown" card always renders. If expenditure data is unavailable, it will display a styled "missing ingredients" placeholder, mirroring the logic used for the Cost per Outcome card.
2.  **Proportional Audit Indicators:** Update the Master Directory table to calculate the total number of audit checks. The opacity of each pass, warning, and fail indicator will dynamically scale between 20% and 100% based on its proportion of the total checks.
3.  **Intervention Badge Capping:** Limit the rendering of interactive provenance badges in the "Intervention Portfolio" cluster to a maximum of 3 per intervention type, preventing visual clutter while maintaining sufficient verifiability.

## Impact
- **Affected specs:** `ui`
- **Affected code:** - `web/layouts/partials/myth-buster.html`
  - `web/layouts/index.html`
  - `web/layouts/partials/itn-scorecard.html`