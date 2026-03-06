## Why
Due to the generative and non-deterministic nature of LLMs, the data extraction pipeline can occasionally produce structurally valid but mathematically or logically inaccurate data (e.g., extracting a highly inflated "Cost per Outcome" due to misidentified populations). Currently, PRISM lacks a staging environment, meaning unverified AI outputs can flow directly to the live production site. To protect the platform's credibility as an Effective Altruism advisory tool, we must implement a "fail-closed" Human-In-The-Loop (HITL) review gate.

## What Changes
1. **Database State Management:** Add a `publish_status` field to the PocketBase `organisations` collection, strictly enforcing a default state of `draft`.
2. **Workflow Reset Trigger:** Configure the n8n orchestration pipeline to explicitly reset the `publish_status` to `draft` whenever it updates an organisation's impact or financial data, forcing re-verification of new extractions.
3. **Hugo Draft Mapping:** Update the Markdown stub generation logic (both in n8n and `scripts/generate_stubs.py`) to map the PocketBase `publish_status` to Hugo's native `draft: true/false` frontmatter.
4. **Analyst Review Loop:** Establish a local operational workflow where analysts use `hugo server -D` to preview and QA drafts visually, manually correct JSON values in the PocketBase Admin UI, approve the records, and sync the clean data to the filesystem via `sync_pb_to_fs.py` prior to deployment.

## Impact
- **Affected specs:** `architecture`, `audit-workflows`
- **Affected code:** `pocketbase/migrations/*`, `scripts/generate_stubs.py`, `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`