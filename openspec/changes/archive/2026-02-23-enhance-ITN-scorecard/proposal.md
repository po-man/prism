# Change: UI Enhancement for ITN Scorecard and Impact Pathways

## Why
Providing raw financial data and a binary checklist is insufficient for promoting Effective Altruism. Users naturally default to evaluating charities by administrative overhead, a flawed metric that encourages the "Starvation Cycle." We must proactively guide donor psychology. By restructuring the UI into a narrative flow—starting with an ITN (Importance, Tractability, Neglectedness) scorecard, visualizing the Logic Model, and contextualizing overhead against actual Cost-per-Outcome—we empower donors to make decisions based on *Value for Money* and counterfactual impact.

## What Changes
- **The ITN Scorecard:** A new hero component at the top of the charity profile summarizing the scale of the problem (Importance), the rigor of evidence (Tractability), and the funding sources (Neglectedness).
- **The Impact Pathway:** A visual flowchart replacing the generic "About Us" section, dynamically rendering Inputs, Activities, Outputs, Outcomes, and the Counterfactual Baseline.
- **The Overhead Myth-Buster:** A dedicated UI section pairing the traditional "Program vs. Admin" pie chart side-by-side with the "Estimated Cost per Outcome", complete with educational tooltips explaining why low overhead does not guarantee high impact.
- **Checklist Grouping:** Refactoring the existing audit checklist to group `<details>` elements under distinct headers (Financial Health, Governance, Impact Rigor) for scannability.

## Impact
- **Affected specs:** `ui`
- **Affected code:** - `web/layouts/_default/single.html`
  - `web/assets/main.css` (Tailwind updates if necessary)