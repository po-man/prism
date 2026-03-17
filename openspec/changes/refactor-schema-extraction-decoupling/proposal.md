## Why
As PRISM's data schemas (`impact.schema.json`, `financials.schema.json`, etc.) have evolved to capture granular, EA-aligned metrics, their complexity has triggered a critical bottleneck in the Gemini API. Specifically, deep nesting, extensive `enum` arrays, and long property names cause the model's finite state machine (FSM) compiler to throw a "too many states for serving" error, halting the orchestration pipeline. To resolve this without compromising our strict Validation Schemas in PocketBase, we must decouple the schema sent to the LLM (Extraction Schema) from our Single Source of Truth (Validation Schema).

## What Changes
- **Dynamic Schema Generation:** Create a new build script (e.g., `scripts/generate_extraction_schemas.py`) that derives lightweight Extraction Schemas directly from the canonical Validation Schemas.
- **Selective Field Pruning:** The script will programmatically strip out downstream fields that the LLM cannot extract (e.g., `resolved_url` inside the `source` object), while retaining fields the LLM must populate (like `source_index` and `search_result_index`).
- **Enum Transformation:** The script will flatten FSM-heavy `enum` arrays into standard `string` types. It will enforce the constraints via prompt engineering by automatically appending the allowed enum values to the field's `description`.
- **Property Name Shortening:** We will introduce a custom `x-extract-key` property into the Validation Schemas for overly long field names. The build script will swap the long key for this shortened key and prepend the humanised original key name to the `description` (e.g., `"description": "Unintended Consequences Reported: Disclosure of..."`) to maintain semantic clarity for the LLM.
- **Payload Reversal in `utils_api`:** Implement a deterministic key-reversal mechanism within the `utils_api` microservice. Before validating the LLM's extraction payload against the strict Validation Schema, the service will dynamically read the `x-extract-key` definitions and map the abbreviated keys back to their canonical long-form names.
- **Orchestrator Updates:** Update the n8n "Charity Analysis" workflow to read the compiled Extraction Schemas for Prompt Injection, while continuing to pass the canonical Validation Schemas to the `utils_api` endpoints.

## Impact
- **Affected specs:** `architecture`, `data-schemas`, `audit-workflows`
- **Affected code:** - `schemas/v1/*.schema.json` (Adding `x-extract-key` metadata)
  - `scripts/generate_extraction_schemas.py` (New script)
  - `utils_api/app/services/schema_mapper.py` (New reversal logic)
  - `utils_api/app/routers/validation.py` and `utils_api/app/routers/audit.py`
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json` (Updating file read paths for prompt injection)