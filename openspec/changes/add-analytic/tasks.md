# Implementation Tasks

## 1. Schema & Data Structure
- [x] 1.1 Create `schemas/v1/analytics.schema.json` defining the checklist array (pass/fail, significance, details).
- [x] 1.2 Update PocketBase `organisations` collection to include the `analytics` JSON field.

## 2. Logic Layer (utils_api) Enhancement
- [x] 2.1 Implement `/audit` endpoint in `utils_api/app/main.py`.
- [x] 2.2 Develop core audit functions:
    - `check_reserve_cap`: `lsg_reserve_amount / operating_expenditure` (Fail if > 0.25).
    - `check_liquidity`: `net_current_assets / monthly_operating_expenses` (Fail if < 3).
    - `check_remuneration`: Check for presence of `rem_pkg_review_report`.
- [x] 2.3 Implement the registry pattern to execute all checks and return a unified result object.

## 3. n8n Workflow Integration
- [x] 3.1 Add an HTTP node "Compute Audit Analytics" after the final extraction merge.
- [x] 3.2 Update "Update Charity" nodes to persist the returned audit results.

## 4. UI Layer (Hugo)
- [x] 4.1 Create Tailwind CSS components for the expandable checklist items.
- [x] 4.2 Implement Hugo template logic to sort items by significance (HIGH > MEDIUM > LOW) and status (FAILED first).
- [x] 4.3 Add visual "Traffic Light" indicators for HIGH-significance failures.