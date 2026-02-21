# openspec/changes/enhance-audit-check-list/tasks.md

## 1. Schema Updates (data-schemas)
- [x] 1.1 Modify `schemas/v1/impact.schema.json` to update the `evidence_quality` enum to reflect the new EA hierarchy: `["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]` (replacing the old High/Medium/Low).
- [x] 1.2 Modify `schemas/v1/impact.schema.json` to add `maxLength` constraints (e.g., `maxLength: 150`) to narrative fields like `context_qualifier` and `counterfactual_baseline.description` to programmatically enforce UI-friendly brevity.

## 2. Prompt Engineering (n8n)
- [x] 2.1 Update `n8n/prompt-templates/impact.system.md` to instruct the LLM to generate concise, short-string summaries for `context_qualifier` and `description` fields to comply with the new schema limits.
- [x] 2.2 Update `n8n/prompt-templates/impact.user.md` to reinforce the extraction of specific target populations rather than vague statements, and ensure it maps exactly to the new `evidence_quality` enums.

## 3. Audit Logic Implementation (utils_api)
- [x] 3.1 Create `utils_api/app/audits/impact.py`.
- [x] 3.2 Implement `check_evidence_quality(record)`. Scan `severity_dimensions`; pass if at least one is `"RCT/Meta-Analysis"` or `"Quasi-Experimental"`, flag as warning if only `"Anecdotal"` or `"None"`. Set significance to HIGH.
- [x] 3.3 Implement `check_counterfactual_baseline(record)`. Pass if `counterfactual_baseline.description` and `value` are non-null and logically populated. Set significance to MEDIUM.
- [x] 3.4 Implement `check_cost_per_outcome(record)`. Divide `financials.data.expenditure.program_services` by the highest `population` or `quantitative_data.value`. Handle `ZeroDivisionError` and missing data gracefully. Set status to `null` (informational only).
- [x] 3.5 Implement `check_funding_neglectedness(record)`. Calculate `income.government_grants / income.total`. Flag as warning ("Low Neglectedness") if > 80%. Pass ("High Neglectedness") if < 40%. Set significance to MEDIUM.

## 4. Orchestration & Testing
- [ ] 4.1 Register the 4 new functions in `utils_api/app/audits/registry.py` under a new "Impact Awareness" block.
- [ ] 4.2 Add unit tests in `utils_api/tests/test_audit.py` to verify the new impact checks handle edge cases (e.g., missing `impact` data, zero program expenses, and the new schema enum values).