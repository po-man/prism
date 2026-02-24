## 1. Schema Updates
- [x] 1.1 Update `schemas/v1/impact.schema.json` to replace human-centric demographics with animal species types (`companion`, `farmed`, `wild`) and intervention methods.
- [x] 1.2 Update `schemas/v1/financials.schema.json` to generalize reserve parameters (remove strict SWD LSG requirements).
- [x] 1.3 Delete `schemas/v1/governance.schema.json`.
- [x] 1.4 Update `utils_api/app/schemas/organisation.py` to remove the `governance` property and validate the updated `impact` and `financials` models.

## 2. Prompt Engineering
- [x] 2.1 Rewrite `n8n/prompt-templates/impact.system.md` to establish the EA/Animal Advocacy persona and ITN evidence hierarchy.
- [x] 2.2 Rewrite `n8n/prompt-templates/impact.user.md` to guide Gemini on extracting animal welfare metrics.
- [x] 2.3 Rewrite `n8n/prompt-templates/financials.system.md` to remove SWD-specific instructions and focus on general Section 88 reporting.
- [x] 2.4 Delete `n8n/prompt-templates/governance.system.md` and `governance.user.md`.

## 3. Python Audit Engine (`utils_api`)
- [ ] 3.1 Implement `check_cause_area_neglectedness` in `utils_api/app/audits/impact.py` focusing on species neglectedness.
- [ ] 3.2 Refactor `check_reserve_cap` and `check_liquidity` in `utils_api/app/audits/financial.py` to handle standard non-profit financial structures.
- [ ] 3.3 Delete `utils_api/app/audits/governance.py`.
- [ ] 3.4 Update `utils_api/app/audits/registry.py` to include the new checks and remove governance checks.
- [ ] 3.5 Write pytest coverage for the new animal-centric audit functions.

## 4. n8n Workflow Refactoring
- [ ] 4.1 Create a PocketBase migration to establish a `target_registry` collection for animal charities. Remove the `rem_pkg_review_report` field from the `organisations` collection.
- [ ] 4.2 Modify `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json` (Main Pipeline):
  - [ ] 4.2.1 Delete the SWD HTTP/HTML scraper nodes and replace with a node that queries the PocketBase `target_registry`.
  - [ ] 4.2.2 Delete all governance-related branches (`Call 'Prompt Injection' - Governance`, `Extract Governance Metrics`, `Schema Validation (Governance)`).
  - [ ] 4.2.3 Ensure "If" nodes robustly handle missing `financial_report` or `annual_report` (Impact) URLs, passing empty JSON to the `utils_api` payload if skipped, preventing pipeline failure.

## 5. UI/UX (Hugo)
- [ ] 5.1 Update `web/layouts/partials/itn-scorecard.html` to visualize the new animal beneficiary data and EA neglectedness logic.
- [ ] 5.2 Update `web/layouts/partials/impact-pathway.html` to gracefully handle animal metrics.
- [ ] 5.3 Ensure `web/layouts/partials/audit-checklist.html` no longer expects or breaks on missing Governance data.