## 1. Orchestration Logic Refactoring (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [x] 1.1 Open the Charity Analysis workflow and sever the parallel connections originating from the `Exists? (Financials+Impact)` node that concurrently trigger the four impact extraction branches.
- [x] 1.2 Re-route the workflow to execute sequentially: Connect the output of `Schema Validation (Impact - Beneficiaries)` to the input of `Call 'Prompt Injection' - Impact - Interventions`.
- [x] 1.3 Chain the remaining branches similarly: `Schema Validation (Impact - Interventions)` $\rightarrow$ `Call 'Prompt Injection' - Impact - Metrics`, and `Schema Validation (Impact - Metrics)` $\rightarrow$ `Call 'Prompt Injection' - Impact - Transparency`.

## 2. Gemini API Payload Updates (Chat History)
- [x] 2.1 Edit the `Extract Impact - Interventions` HTTP Request node. Update the `jsonBody` to format the `contents` array as a conversation. Append the Beneficiaries prompt (`"role": "user"`) and the validated Beneficiaries JSON output (`"role": "model"`) before the Interventions prompt.
- [x] 2.2 Edit the `Extract Impact - Metrics` HTTP Request node. Update the `contents` array to include the history of both the Beneficiaries and Interventions prompts and their respective model outputs to preserve the thought signature.
- [x] 2.3 Edit the `Extract Impact - Transparency` HTTP Request node. Update the `contents` array to include the full conversational history (Beneficiaries, Interventions, and Metrics prompts and outputs).

## 3. Data Assembly & Merge Node Cleanup
- [x] 3.1 Locate the 4-way `Merge` node (id: `62877729-bd54-4f43-865f-5e1cd5631407`) that previously awaited all parallel branches.
- [x] 3.2 Delete this 4-way Merge node.
- [x] 3.3 Connect the final output of `Schema Validation (Impact - Transparency)` directly to the `Storage API - Update Charity - Impact` node.
- [x] 3.4 Update the `Storage API - Update Charity - Impact` node's `bodyParameters`. Since the flow is now serialised, ensure it references the sequentially accumulated data from the upstream nodes (e.g., using `$node["Schema Validation (Impact - Beneficiaries)"].json.data` for the beneficiaries portion) rather than relying on a single merged array index.