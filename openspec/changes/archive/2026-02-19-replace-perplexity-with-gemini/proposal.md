# Change: Replace Perplexity with Gemini API

## Why
Currently, the data extraction pipeline relies on the Perplexity API for parsing financial reports and executing web searches. However, financial reports from Hong Kong NGOs often contain complex, unstructured tables that are difficult to parse accurately using intermediate text-only OCR. Google's Gemini API offers a native Multimodal API capable of processing raw PDFs directly, which drastically improves layout understanding and financial data extraction. Additionally, Gemini's "Grounding with Google Search" provides a native, highly accurate method for retrieving real-time reputational risk data and metadata, eliminating the need for a separate search agent infrastructure.

## What Changes
- **API Provider:** Transition all AI inference nodes in `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json` from Perplexity to Gemini (e.g., `gemini-2.0-flash` or `gemini-1.5-pro`).
- **Document Intelligence (PDFs):** Update the "Extract Financials", "Extract Impact Metrics", and "Extract Governance Metrics" nodes to pass the raw PDF files (via base64 inline data or the Gemini Files API) directly to the model, rather than relying solely on the prior OCR text extraction.
- **Web Search Intelligence:** Update the "Extract Risk" and "Find Metadata" nodes to enable the `googleSearch` tool within the Gemini API payload for real-time grounding.
- **Structured Outputs:** Refactor the HTTP requests to utilize Gemini's `response_mime_type: "application/json"` and `response_schema` parameters to enforce strict schema adherence, replacing the need for prompt-based JSON coercion.

## Impact
- **Affected specs:** `audit-workflows`
- **Affected code:**
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`
  - `docker-compose.yml` (Environment variables)
  - `n8n/prompt-templates/*`