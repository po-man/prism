# openspec/changes/add-donor-transparency-ui/tasks.md

## 1. Audit Engine Updates (`utils_api`)
- [x] 1.1 Modify `utils_api/app/audits/impact.py` -> `check_cost_per_outcome`. Add logic to divide 1000 by the calculated `cost_per` and format it to 1 decimal place.
- [x] 1.2 Append the translated string to the `calculation` output.
- [x] 1.3 Update `utils_api/tests/test_audit_impact.py` to assert the presence of the "$1,000 donation" string in the test cases.

## 2. UI / Hugo Updates (`web`)
- [x] 2.1 Update `web/layouts/_default/single.html` to inject the "Data Provenance" icon row below the charity name/risk badge. Add Go template logic checking `if .financial_report` and `if .annual_report` to toggle CSS opacity classes.
- [x] 2.2 Update `web/layouts/partials/itn-scorecard.html` to map `.beneficiary_type` variables to specific SVG icons (e.g., using FontAwesome or Heroicons SVG paths) inside the "Importance" or "Neglectedness" cards.
- [x] 2.3 Update `web/layouts/partials/myth-buster.html` to visually highlight the new $1,000 translation text returned from the `check_cost_per_outcome` calculation, styling it as a high-impact callout box.