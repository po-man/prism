# Implementation Tasks

## 1. Prompt Engineering (n8n)
- [ ] 1.1 Update `n8n/prompt-templates/impact.system.md` to instruct the LLM to generate concise, short-string summaries (under 150 characters) for `context_qualifier` and `description` fields to ensure UI compatibility.
- [ ] 1.2 Update `n8n/prompt-templates/impact.user.md` to reinforce the extraction of specific target populations rather than vague, overarching statements.

## 2. Audit Logic Implementation (utils_api)
- [ ] 2.1 Create `utils_api/app/audits/impact.py`.
- [ ] 2.2 Implement `check_evidence_quality(record)`. Scan `severity_dimensions`; pass if at least one is "High" or "Medium", flag as warning if only "Low" or "Anecdotal". Set significance to HIGH.
- [ ] 2.3 Implement `check_counterfactual_baseline(record)`. Pass if `counterfactual_baseline.description` and `value` are non-null and logically populated. Set significance to MEDIUM.
- [ ] 2.4 Implement `check_cost_per_outcome(record)`. Divide `financials.data.expenditure.program_services` by the highest `population` or `quantitative_data.value`. Handle `ZeroDivisionError` and missing data gracefully. Set status to `null` (informational only).
- [ ] 2.5 Implement `check_funding_neglectedness(record)`. Calculate `income.government_grants / income.total`. Flag as warning ("Low Neglectedness") if > 80%. Pass ("High Neglectedness") if < 40%.

## 3. Orchestration & Testing
- [ ] 3.1 Register the 4 new functions in `utils_api/app/audits/registry.py` under a new "Impact Awareness" block.
- [ ] 3.2 Add unit tests in `utils_api/tests/test_audit.py` to verify the new impact checks handle edge cases (e.g., missing `impact` data, zero program expenses).