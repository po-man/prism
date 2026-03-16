## Why
Analysis of recent data outputs (e.g., Blue Cross of India) reveals that the LLM frequently hallucinates empty `explicit_unit_cost` objects (amounting to 0) when no unit cost is stated. Due to limitations in our JSON schema validator regarding nullable objects, this bypasses our validation and causes the `utils_api` to calculate an erroneous Cost Per Outcome of $0.00. Furthermore, while the system successfully extracts verifiable quotes for transparency indicators (like euthanasia statistics), these quotes are currently sequestered in the JSON payload and not surfaced to the end-user, limiting the audibility of the "Epistemic Humility" checks. Finally, the currency field lacks strict ISO formatting guidelines, leading to unpredictable outputs like `$`.

## What Changes
- **Impact Schema (`schemas/v1/impact.schema.json`):** - Add the `source` object definition to `operating_scope` and `explicit_unit_cost` for strict provenance tracking.
  - Amend the `currency` property description to enforce 3-letter ISO 4217 codes.
  - Convert the inner properties of `explicit_unit_cost` to nullable types (`["number", "null"]`, `["string", "null"]`) to prevent default-zero hallucinations.
- **LLM Prompts (`n8n/prompt-templates/impact.system.md`):** Update extraction instructions to enforce the new schema constraints and explicitly forbid hallucinating `0` for missing costs.
- **Audit Logic (`utils_api/app/audits/transparency.py`):** Modify the transparency audit functions to inject the extracted `source.quote` directly into the `details.elaboration` field, automatically rendering it in the UI.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/impact.schema.json`, `n8n/prompt-templates/impact.system.md`, `utils_api/app/audits/transparency.py`