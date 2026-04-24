## Why
To make the PRISM interface more accessible to layman users, we must reduce the use of academic Effective Altruism jargon (e.g., "Neglectedness", "Importance") and eliminate redundant "Annual" tags, as the temporal bounding is already established globally for the report. Furthermore, the intervention portfolio currently lacks visual hierarchy; applying tier-coloured badges will allow donors to immediately parse the tractability and leverage of a charity's activities. Finally, the master table must accurately represent "unspecified" beneficiaries to maintain complete data provenance.

## What Changes
1. **Jargon Removal:** Strip "(Neglectedness)" and "(Importance)" from the Master Table headers and the "How to Read" section.
2. **Temporal Tags:** Remove the "Annual" badges from the ITN Scorecard and IES Scorecard to reduce visual clutter.
3. **Master Table Iconography:** Implement the logic to render the `unspecified-animals.svg` icon dynamically within the Target Species column of the Master Table, aligning with the logic currently used on the individual organisation pages.
4. **Intervention Portfolio Styling:** Refactor the tractability portfolio loop to assign dynamic Tailwind CSS classes to intervention badges based on their Leverage Tier (Tier 1: Purple, Tier 2: Blue, Tier 3: Grey). Add a corresponding legend styled similarly to the IES breakdown key.

## Impact
- **Affected specs:** `ui`
- **Affected code:** - `web/layouts/index.html`
  - `web/layouts/partials/index-how-to-read.html`
  - `web/layouts/partials/itn-scorecard.html`
  - `web/layouts/partials/ies-scorecard.html`