## 1. Environment and Configuration
- [x] 1.1 Update `docker-compose.yml` and `.env` configurations to replace `CREDENTIALS_PERPLEXITY_API_KEY` with `CREDENTIALS_GEMINI_API_KEY`.
- [x] 1.2 Add the Gemini API credentials to `n8n` (via Generic HTTP Auth or native Google Gemini node).

## 2. Document Intelligence (Multimodal PDF Parsing)
- [x] 2.1 Refactor the `Download PDF & Extract Text` (or `Base64` conversion) nodes in `workflows/SUjUpjve9Vj6aJSbbuIWL.json` to prepare PDF data for Gemini instead of routing through Tesseract/Stirling-PDF text extraction.
- [x] 2.2 Update the "Extract Financials", "Extract Impact Metrics", and "Extract Governance Metrics" HTTP Request nodes to call the Gemini API (`generateContent` endpoint).
- [x] 2.3 Modify the payload of these nodes to pass the PDF document either via `inlineData` (for files < 20MB) or the Gemini Files API.
- [x] 2.4 Configure the `responseMimeType` to `application/json` and inject the loaded schemas from `/schemas/v1/*.schema.json` into the `responseSchema` field to guarantee structured outputs.

## 3. Web Search Intelligence (Search Grounding)
- [x] 3.1 Update the "Find Metadata" and "Extract Risk" nodes to call the Gemini API.
- [x] 3.2 Add the `tools: [{"google_search": {}}]` configuration to the Gemini API request body to enable Grounding with Google Search.
- [x] 3.3 Ensure the prompt explicitly instructs the model to use the search results to find recent news, scandals, or specific metadata related to the charity.

## 4. Prompt Engineering and Cleanup
- [x] 4.1 Update `n8n/prompt-templates/*.user.md` and `*.system.md` templates. Remove generic instructions like "Return strictly valid JSON" since this is now handled natively by the API's schema constraints.
- [x] 4.2 Test the new Gemini nodes against the `utils_api/validate` microservice to ensure the output perfectly matches the established Pydantic schemas.
- [x] 4.3 Remove deprecated Perplexity API credentials from the repository.