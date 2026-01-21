# Proposal: Audit Automation Agents (Cost-Optimized)

## Why
The static `governance.schema.json` requires an intelligent ingestion engine. However, "Agentic" workflows are expensive (LLM tokens) and slow (web scraping). To prevent budget drain during development and partial failures, the system must be **idempotent**. If the workflow crashes at step 5, re-running it should simply load the saved results of steps 1-4 from disk rather than re-querying the APIs.

## What Changes
- **New Capability:** `audit-workflows`
- **Architecture:** "Hub-and-Spoke" with **State Persistence**:
    - **Scout Agent:** Locates Annual Reports. Caches result to `data/cache/{id}_scout.json`.
    - **Extractor Agent:** Extracts Financials/LSG data. Caches result to `data/cache/{id}_extracted.json`.
    - **Risk Agent:** Scans news. Caches result to `data/cache/{id}_risk.json`.
- **Scope Refinement:**
    - **REMOVED:** Cap 622 (Companies Ordinance) checks. The system will focus purely on Financial Health (Accounting Standards) and LSG Manual compliance.

## Impact
- **Cost Efficiency:** Re-runs are effectively free for steps that have already passed.
- **Debugging:** Developers can inspect the intermediate `data/cache/` files to isolate agent failures.
- **Data Flow:** Intermediate JSONs are merged into the final `data/organisations/{id}.json`.