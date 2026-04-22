## Why
Currently, the n8n orchestrator executes the four branches of impact data extraction (Beneficiaries, Interventions, Metrics, Transparency) in parallel. While this parallelisation optimises for speed, it creates isolated context windows. The LLM evaluates the charity's metrics without the foundational context of who the beneficiaries are, or evaluates transparency without knowing the specific interventions. By serialising the extraction into a "chat-like" mode, we allow the Gemini model to build a cumulative, coherent internal representation (thought signature) of the charity's impact logic model. This mimics a human auditor's sequential analysis, fundamentally improving extraction accuracy, reducing intra-domain contradictions, and increasing the fidelity of complex EA alignment evaluations.

## What Changes
1. **Workflow Sequencing:** Refactor the `SUjUpjve9Vj6aJSbbuIWL.json` n8n workflow to chain the four impact extraction HTTP Request nodes sequentially: Beneficiaries $\rightarrow$ Interventions $\rightarrow$ Metrics $\rightarrow$ Transparency.
2. **Context Chaining (Chat History):** Modify the `jsonBody` of the Gemini API HTTP requests for the latter three steps. Instead of sending a single user prompt, the `contents` array will be constructed as a multi-turn conversation. It will include previous user prompts and the model's previous extracted JSON responses (`"role": "model"`), ensuring the LLM retains its thought signature and prior contextual conclusions.
3. **Pipeline Consolidation:** Remove the 4-way parallel merge node. The validation, normalisation, and provenance resolution steps will be triggered sequentially as the data payload is enriched step-by-step, culminating in the final update to the PocketBase data vault.

## Impact
- **Affected specs:** `audit-workflows`
- **Affected code:** `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`