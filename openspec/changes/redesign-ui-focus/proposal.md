## Why
The current platform UI heavily relies on rigid Effective Altruism (EA) terminology, such as the "ITN Scorecard" (Importance, Tractability, Neglectedness) and definitive "Impact Equivalency Scores" (IES). While this strict analytical framework is excellent for the backend audit engine, presenting it as an absolute leaderboard on the frontend can be alienating or misleading for retail donors. We need to shift the UI focus to make the data more public-friendly: highlighting objective demographics, visualising the "ingredients" of impact calculations, and de-emphasising definitive "golden scores" and tiered hierarchies.

## What Changes
1. **Master Directory Cleanup:** Remove the "Highest Leverage (Tractability)" column entirely from the master comparative table to prevent users from reducing complex charities to a single "Tier" ranking.
2. **ITN Scorecard Refactoring:** - Rename the "ITN Scorecard" component to "Impact Profile".
   - Redesign the "Tractability / Highest Intervention Leverage" card into a "Verified Activities" card. Instead of emphasising the "Tier" hierarchy, it will present the verified interventions as an accessible, visually appealing cluster of badges/tags.
3. **IES Scorecard Contextualisation:** Add explanatory text to the IES component, clarifying that the score serves purely as a reference point by exposing the "ingredients" of the calculation (Empirical Data and Philosophical Assumptions). Concurrently, downsize the visual weight of the final evaluated score to prevent it from being perceived as an absolute truth.

## Impact
- **Affected specs:** `ui`
- **Affected code:** `web/layouts/index.html`, `web/layouts/partials/index-how-to-read.html`, `web/layouts/partials/itn-scorecard.html`, `web/layouts/partials/ies-scorecard.html`