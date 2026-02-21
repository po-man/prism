# Change: Refactor Document Intelligence to use Gemini File API

## Why
Currently, the n8n data extraction pipeline converts downloaded PDFs into base64 strings and attaches them as `inlineData` in the payload for the Gemini API. This approach is bound by a strict 50MB payload limit. Because Hong Kong charities often publish Annual Reports and Financial Statements containing heavy scanned images or extensive bilingual text, these files frequently exceed the 50MB limit, causing the extraction workflows to fail. Migrating to the Gemini File API allows us to process documents up to 2GB. 

Because Gemini URIs expire after 48 hours—which is a different lifecycle than our permanent physical storage in PocketBase—we must isolate the expiration-checking and upload logic into a dedicated sub-workflow to keep the main orchestration clean and idempotent.

## What Changes
- **PocketBase Schema Update:** Add `gemini_file_uri` (text) and `gemini_file_uploaded_at` (date) to the `source_artifacts` collection to keep track of cloud-hosted files.
- **New Sub-Workflow (`Ensure Gemini URI`):** A dedicated n8n workflow that takes a `source_artifact` ID. It checks if the `gemini_file_uploaded_at` timestamp is within a safe window (< 46 hours). If expired or missing, it downloads the raw PDF from PocketBase, uploads it to the Gemini File API, updates the PocketBase record with the new URI and timestamp, and returns the valid URI.
- **n8n Main Workflow (LLM Inference):** Replace the local file download nodes with `Execute Workflow` nodes calling the new `Ensure Gemini URI` sub-workflow. Update the "Extract Financials", "Extract Impact Metrics", and "Extract Governance Metrics" nodes to pass `fileData: { fileUri: "..." }` instead of base64 `inlineData`.

## Impact
- **Affected specs:** `audit-workflows`
- **Affected code:**
  - `pocketbase/migrations/*` (New migration required for `source_artifacts`)
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json` (Main Charity Analysis workflow)
  - New n8n workflow file (e.g., `Ensure_Gemini_URI.json`)