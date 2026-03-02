# openspec/changes/update-asia-expansion-and-ui-refinements/proposal.md

## Why
To position PRISM as a fundable MVP for the EA Animal Microgrants, the platform must evolve from a Hong Kong-specific prototype into a pan-Asian evaluation engine capable of capturing highly neglected areas like farm animal advocacy. Furthermore, the current UI and Audit Engine logic undervalues cumulative impact by relying on "max" beneficiary values rather than sums, and dilutes tractability by lacking exact evidence quotes and overwhelming the user with unprioritized activities and "calculation-only" checklist items.

## What Changes
1. **Global Metadata Compatibility:** Deprecate the HK-specific `s88_id` in favor of a universal `registration_id` in the metadata schema and LLM prompts.
2. **Cumulative Impact Logic:** Refactor the Audit Engine (`utils_api`) and the UI (Hugo) to utilize the *sum* of all beneficiary populations for both the "Importance" scorecard and the "Cost per Outcome" Value for Money metric, eliminating the previous "max" logic which undervalued multi-program charities.
3. **Evidence Verifiability:** Enhance the `impact` schema to capture exact `evidence_quote` strings directly from source documents. The UI will surface these quotes in the Tractability card and Audit Checklist to provide immediate, verifiable proof of impact claims.
4. **Information Hierarchy (UI):** - Update the Impact Pathway to sort Activities and Outcomes by significance, displaying only the Top 3 by default with an expandable "Show All" toggle.
   - Refine the Audit Checklist to exclude "calculation-only" (status: `null`) items, reducing noise and focusing solely on actionable Pass/Warning/Fail EA criteria.
   - Add tooltips to the Value for Money calculations to increase transparency.

## Impact
- **Affected specs:** `data-schemas`, `ui`, `audit-workflows`
- **Affected code:** `schemas/v1/*`, `n8n/prompt-templates/*`, `utils_api/app/audits/*`, `web/layouts/partials/*`