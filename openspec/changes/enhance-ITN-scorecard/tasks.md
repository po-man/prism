# Implementation Tasks

## 1. ITN Scorecard Implementation (Hugo/HTML)
- [x] 1.1 In `web/layouts/_default/single.html`, add a new "ITN Scorecard" grid section below the Charity Name header.
- [x] 1.2 Bind **Importance**: Display `impact.data.importance_factors.problem_profile.problem_name` and the largest `population` count.
- [x] 1.3 Bind **Tractability**: Display the highest `evidence_quality` found in the severity dimensions array.
- [x] 1.4 Bind **Neglectedness**: Render a visual progress bar (HTML/Tailwind) comparing `government_grants` to `donations` using data from `financials.data.income`.

## 2. Impact Pathway Component (Logic Model)
- [ ] 2.1 Build a horizontal flexbox/grid flowchart component in `single.html`.
- [ ] 2.2 Map `financials.data.expenditure.total` to the **Inputs** node.
- [ ] 2.3 Map `tractability_factors.significant_events` summaries to the **Activities/Outputs** node.
- [ ] 2.4 Map `problem_profile.severity_dimensions` to the **Outcomes** node.
- [ ] 2.5 Add a highlighted callout box rendering the `counterfactual_baseline.description` to explicitly answer "What happens without them?".

## 3. The "Overhead vs. Impact" Myth-Buster
- [ ] 3.1 Create a two-column UI card.
- [ ] 3.2 In the left column, display the Administrative vs. Program expenses ratio using a simple CSS/SVG pie chart or segmented progress bar.
- [ ] 3.3 In the right column, extract the `details.calculation` string from the `check_cost_per_outcome` item inside `analytics.check_items`.
- [ ] 3.4 Add an educational tooltip or blockquote explaining that investing in infrastructure (admin) is often required to achieve rigorous outcomes.

## 4. Audit Checklist Refactoring
- [ ] 4.1 Update the Go template `range` loops in `single.html` to group `check_items` by their `category` (Financial Health, Governance, Impact Awareness).
- [ ] 4.2 Render a distinct sub-header for each category to improve scannability, maintaining the existing pass/fail traffic light system.