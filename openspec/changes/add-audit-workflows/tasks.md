## 1. Persistence Layer Setup (PocketBase)
- [ ] 1.1 Add PocketBase to the project's `docker-compose.yml`.
- [ ] 1.2 Create a script to initialize PocketBase collections on first run (`scout_results`, `extractor_results`, `risk_results`, `source_artifacts`).
- [ ] 1.3 Define the **"Query-or-Run" n8n Pattern**:
    - Node A: `HTTP Request` (Query PocketBase for existing record).
    - Node B: `If` (Record Found?).
    - True: Use data from PocketBase response.
    - False: Fetch External -> `HTTP Request` (Write to PocketBase) -> Use new data.

## 2. Scout Agent (Document Discovery)
- [ ] 2.1 Create `workflows/sub_scout.json`.
- [ ] 2.2 **Implement Caching**: Query the `scout_results` collection in PocketBase before calling Perplexity.
- [ ] 2.3 Implement Perplexity "Sonar-Reasoning" node to find the target URL.
- [ ] 2.4 Add "Link Validator" (Head Request) to ensure PDF reachability.
- [ ] 2.5 Save valid output (URL + Year) to the `scout_results` collection.

## 3. Extractor Agent (The Regulatory Brain)
- [ ] 3.1 Create `workflows/sub_extractor.json`.
- [ ] 3.2 **Implement Binary Caching (The Vault)**:
    - Input: `pdf_url` from Scout.
    - Query the `source_artifacts` collection for the PDF.
    - **IF MISSING**: Use HTTP Request (Get Stream) to download the PDF, then use another `HTTP Request` node to upload the binary to a new record in the `source_artifacts` collection.
    - **IF PRESENT**: Use the record's file URL to load the binary from the local PocketBase instance.
- [ ] 3.3 **Implement Text Caching**:
    - Check if the `extractor_results` collection has a record with the extracted text for this run.
    - If no, Parse the **Local PDF Binary** -> Save the raw text to the record.
- [ ] 3.4 Implement **Financial Extraction** (LLM Node):
    - *System Prompt:* "You are a forensic accountant. Extract exact figures from the provided text..."
    - *Schema Mapping:* Map `total_income`, `program_expenses`, `lsg_reserve_amount`.
    - *Constraint:* STRICTLY ignore Cap 622/Director metrics.
- [ ] 3.5 Save structured data to the `extractor_results` collection in PocketBase.

## 4. Risk Agent (Reputation Check)
- [ ] 4.1 Create `workflows/sub_risk.json`.
- [ ] 4.2 **Implement Caching**: Query the `risk_results` collection before searching.
- [ ] 4.3 Implement Search API -> Sentiment Filter.
- [ ] 4.4 Save flags to the `risk_results` collection.

## 5. Orchestration & Merge
- [ ] 5.1 Update `workflows/main_orchestrator.json`.
- [ ] 5.2 Implement `HTTP Request` nodes to query PocketBase for the results from the `scout_results`, `extractor_results`, and `risk_results` collections.
- [ ] 5.3 Implement a `Merge` node to combine the data from the three queries.