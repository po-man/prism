## Why
To effectively demonstrate PRISM as a fundable, high-impact, the UI must facilitate immediate, actionable comparative analysis for donors. The current single-page layout suffers from extreme cognitive overload when scaling beyond a few charities. By introducing a Master Table landing page and dedicated individual profiles, we empower users to quickly compare organizations across the ITN framework (Importance, Tractability, Neglectedness) and Cost per Outcome, making the platform a true decision-support engine.

## What Changes
1. **Branding:** Rename the placeholder "CharityGrader" to "PRISM" across the UI header and metadata.
2. **Architecture (Hugo Data Routing):** Update the data ingestion pipeline so that each validated JSON artifact in `data/organisations/` has a corresponding Markdown stub in `content/audits/`. This allows Hugo to generate individual, routable pages for each charity.
3. **Master Table (Landing Page):** Create a new `list.html` template that iterates over all charities to produce a sortable comparative table. Key columns will include:
   - Organization Name
   - Primary Beneficiary Type (Neglectedness)
   - Scale (Importance - Total Beneficiaries)
   - Evidence Quality (Tractability)
   - Estimated Cost per Outcome
   - Audit Pass/Fail Summary (Miniature traffic light indicators)
4. **Individual Pages:** Refactor `single.html` to display the detailed report card (ITN Scorecard, Impact Pathway, Myth-Buster, and Audit Checklist) for a single organization, identical to the current design but isolated to its own URL.
5. **UI Enhancement (Sorting):** Integrate a lightweight, offline-compatible Vanilla JS table sorter on the landing page, allowing users to explicitly "Sort by Cost per Outcome" or "Sort by Neglectedness," directly supporting EA principles.

## Impact
- **Affected specs:** `ui`, `architecture`
- **Affected code:** `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`, `web/layouts/_default/baseof.html`, `web/layouts/audits/list.html` (new), `web/layouts/audits/single.html` (refactored).