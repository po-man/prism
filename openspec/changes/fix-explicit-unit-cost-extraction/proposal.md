# Change: Restrict Explicit Unit Cost Extraction to Per-Animal Outcomes

## Why
Currently, the `calculate_cost_per_outcome` function in the `utils_api` directly translates values from the `explicit_unit_costs` array into the `HIGH` confidence "Cost Per Outcome (USD)" metric. However, because the LLM prompt loosely allows extracting the cost to "deliver an intervention," the system frequently captures aggregate budgets, monthly team costs, and total grant awards (e.g., a €195,000 grant). This results in wildly inaccurate unit costs being displayed on the UI, destroying the integrity of the Value for Money assessment for EA donors. 

## What Changes
1. **Prompt Engineering:** Update the `impact.system.md` system prompt to strictly limit `explicit_unit_costs` to costs per *individual animal*. We will explicitly prohibit the extraction of aggregate budgets, total grant awards, monthly running costs, or overall fundraising campaign goals into this array.

## Impact
- **Affected specs:** `audit-workflows`
- **Affected code:** `n8n/prompt-templates/impact.system.md`