# Proposal: Audit Analytics and UI Visualization

## Why
Raw data extraction is not enough to empower donors. We need to transform JSON integers into actionable insights. This change introduces the "Binary Audit Checklist" model, moving away from subjective scoring to verifiable compliance checks. It ensures that high-priority failures (like LSG reserve violations) are immediately visible to users while maintaining a transparent "audit trail" for every calculation.

## What Changes
- **New Capability:** `ui-presentation` for rendering the checklist.
- **Logic Layer:** Expansion of `utils_api` to include a registry of audit check functions (e.g., `check_reserve_cap`, `check_liquidity`).
- **Data Schema:** Introduction of `schemas/v1/analytics.schema.json` to store the checklist results.
- **Workflows:** A new "Compute Analytics" node in the n8n main workflow to trigger the audit logic.
- **UI Logic:** Implementing a priority-sorting algorithm where failed HIGH-significance items are displayed first.

## Impact
- **utils_api:** Significant new Python logic for financial calculations.
- **Hugo:** New templates to handle the expandable checklist UI components.
- **PocketBase:** New `analytics` JSON field added to the `organisations` collection.