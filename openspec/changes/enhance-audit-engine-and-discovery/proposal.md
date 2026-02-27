# openspec/changes/enhance-audit-engine-and-discovery/proposal.md

# Change: Enhance Audit Engine and Implement Discovery Landing Page

## Why
While the current platform evaluates charities individually, EA philanthropy is inherently comparative: donors seek the *most* effective, *most* transparent, and *most* neglected opportunities. Currently, the system lacks a master index page to compare charities side-by-side. Furthermore, severe risks (like the scandals found in our sample data) and lack of financial transparency are only passively displayed; they must explicitly trigger Pass/Fail logic within the audit checklist to hold organizations accountable.

## What Changes
- **Expanded Audit Engine:** Introduce new programmatic checks in the Python `utils_api` for Data Transparency (Pass if financials exist, Fail if not) and Reputational Risk (Fail on High Risk, Warning on Medium, Pass on Low).
- **Schema Updates:** Update the `analytics.schema.json` to accept "Data Transparency" as a valid checklist category.
- **Charity Discovery Landing Page:** Transform the static root index (`_index.md` / `index.html`) into a dynamic, offline-capable dashboard. It will list all evaluated charities and use Vanilla JS to allow users to sort and filter by EA pillars (Highest Neglectedness, Best Evidence Quality, Lowest Risk).

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/analytics.schema.json`, `utils_api/app/audits/registry.py`, `utils_api/app/audits/transparency.py` (new), `utils_api/app/audits/risk.py` (new), `web/layouts/index.html` (new), `web/static/js/filter.js` (new).