## 1. Persistence Layer Setup (PocketBase)
- [x] 1.1 Add PocketBase to the project's `docker-compose.yml`.
- [x] 1.2 Create a script to initialize PocketBase collections on first run (`organisations`, `reports`, `source_artifacts`).
- [x] 1.3 Define the **"Query-or-Run" n8n Pattern**:
    - Node A: `HTTP Request` (Query PocketBase for existing record).
    - Node B: `If` (Record Found?).
    - True: Use data from PocketBase response.
    - False: Fetch External -> `HTTP Request` (Write to PocketBase) -> Use new data.

## 2. Scout Agent (Document Discovery)
- [x] 2.1 Create `workflows/SUjUpjve9Vj6aJSbbuIWL.json` (Charity Analysis) which includes scouting logic.
- [x] 2.2 **Implement Caching**: Queries the `reports` collection in PocketBase before scraping.
- [x] 2.3 Implement Perplexity "Sonar-Reasoning" node to find the target URL (for domains).
- [x] 2.4 Add "Link Validator" (If node) to check if a URL exists before downloading.
- [x] 2.5 Save valid output (URL, organisation, type) to the `reports` collection.

## 3. Extractor Agent (The Regulatory Brain)
- [x] 3.1 Create `workflows/dM945Azme2TNMwoX.json` (Download PDF & Extract Text).
- [x] 3.2 **Implement Binary Caching (The Vault)**:
    - Input: `pdf_url` from Scout.
    - The sub-workflow downloads the PDF and uploads the binary to a new record in the `source_artifacts` collection.
- [x] 3.3 **Implement Text Caching**:
    - The sub-workflow uses a PDF API to extract text and saves it to the `source_artifacts` record.
- [x] 3.4 Implement **Financial, Impact, and Governance Extraction** (LLM Node):
    - *System Prompt:* "You are a forensic accountant. Extract exact figures from the provided text..."
    - *Schema Mapping:* Maps various fields for financials, impact, and governance.
- [x] 3.5 Save structured data to the `organisations` collection in PocketBase.

## 4. Risk Agent (Reputation Check)
- [x] 4.1 Logic integrated into the main `Charity Analysis` workflow.
- [x] 4.2 **Implement Caching**: The "Query-or-Run" pattern checks if the `risk` field in the `organisations` collection already exists.
- [x] 4.3 Implement Perplexity AI search to find negative news or reputational flags.
- [x] 4.4 Save structured results to the `risk` field in the `organisations` collection.

## 5. Orchestration & Merge
- [x] 5.1 Create `workflows/SUjUpjve9Vj6aJSbbuIWL.json` as the main orchestrator.
- [x] 5.2 Implement `HTTP Request` nodes to query and update PocketBase for `reports` and `organisations`.
- [x] 5.3 Implement `Merge` nodes to handle different execution paths and wait for parallel tasks.