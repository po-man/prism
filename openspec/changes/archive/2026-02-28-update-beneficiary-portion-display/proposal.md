# Change: Calculate and Display Proportional Beneficiary Breakdowns

## Why
Currently, the PRISM ITN Scorecard displays a binary visual indicator (badges) for the types of animals a charity helps (Companion, Farmed, Wild) and the `utils_api` awards a "Pass" for Neglectedness if *any* high-neglectedness species is present. This creates an EA evaluation loophole: a charity dedicating 99% of its resources to saturated areas (companion animals) and 1% to neglected areas (wildlife) receives the same Neglectedness status as a 100% wildlife charity. To provide an accurate, data-driven EA assessment, the system must evaluate and display the proportional breakdown of concerned animals based on exact population data.

## What Changes
- **Data Integrity (No Schema Change):** We will rely strictly on the existing `population` integer field within the `impact.schema.json` -> `beneficiaries` array to maintain the vault as a source of raw, un-inferred facts. 
- **Intelligence Prompts (`n8n`):** Update `impact.system.md` to instruct the LLM to explicitly seek and extract exact `population` counts disaggregated by `beneficiary_type` whenever multiple animal types are supported.
- **Audit Engine (`utils_api`):** Refactor the `check_cause_area_neglectedness` logic to calculate the total population across all beneficiary types. It will then determine the ratio of high-neglectedness animals (farmed/wild) to low-neglectedness animals (companion) to assign a weighted Pass, Warning, or Fail status. It will include graceful fallbacks if population data is `null`.
- **UI/UX (`web`):** Update the `itn-scorecard.html` Hugo partial. The UI will use Hugo template math to dynamically sum the total `population` across the `beneficiaries` array, calculate the percentage for each type, and render these percentages next to the respective species badges.

## Impact
- **Affected specs:** `audit-workflows`, `ui`
- **Affected code:** `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/impact.py`, `utils_api/tests/test_audit_impact.py`, `web/layouts/partials/itn-scorecard.html`