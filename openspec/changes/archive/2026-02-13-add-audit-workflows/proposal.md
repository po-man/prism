# Proposal: Audit Automation Agents (Cost-Optimized)

## Why
The static `governance.schema.json` requires an intelligent ingestion engine. However, "Agentic" workflows are expensive (LLM tokens) and slow (web scraping). To prevent budget drain during development and partial failures, the system must be **idempotent**. If the workflow crashes at step 5, re-running it should simply load the saved results of steps 1-4 from disk rather than re-querying the APIs.

## What Changes
- **New Capability:** `audit-workflows`
- **Architecture:** "Hub-and-Spoke" with **PocketBase for State Persistence**:
    - A local PocketBase datastore will be introduced to manage all intermediate state, replacing the file-based caching system. It provides a unified API for JSON data and binary file storage.
    - **Scout Agent:** Locates Annual Reports. Caches result to a `scout_results` collection in PocketBase.
    - **Extractor Agent:** Extracts Financials/LSG data. Caches structured data to an `extractor_results` collection and downloaded PDFs to a `source_artifacts` collection.
    - **Risk Agent:** Scans news. Caches result to a `risk_results` collection.
- **Scope Refinement:**
    - **REMOVED:** Cap 622 (Companies Ordinance) checks. The system will focus purely on Financial Health (Accounting Standards) and LSG Manual compliance.

## Impact
- **Cost Efficiency:** Re-runs are effectively free for steps that have already passed.
- **Debugging:** Developers can use the PocketBase Admin UI to inspect and manage cached data, providing a much richer debugging experience than inspecting individual files.
- **Data Flow:** The orchestrator will query the various PocketBase collections, merge the results, and write the final output to `data/organisations/{id}.json`.