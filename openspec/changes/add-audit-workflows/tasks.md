## 1. File System Preparation (The Cache Layer)
- [ ] 1.1 Create `data/cache/` directory (git-ignored) for JSON states.
- [ ] 1.2 Create `data/cache/artifacts/` directory (git-ignored) for raw PDF binaries.
- [ ] 1.3 Define the **"Read-or-Run" n8n Pattern**:
    - Node A: `Read File` (Continue on Fail).
    - Node B: `If` (File Exists?).
    - True: Use local data.
    - False: Fetch External -> Write File -> Use new data.

## 2. Scout Agent (Document Discovery)
- [ ] 2.1 Create `workflows/sub_scout.json`.
- [ ] 2.2 **Implement Caching**: Check `data/cache/{id}_scout.json` before calling Perplexity.
- [ ] 2.3 Implement Perplexity "Sonar-Reasoning" node to find the target URL.
- [ ] 2.4 Add "Link Validator" (Head Request) to ensure PDF reachability.
- [ ] 2.5 Save valid output (URL + Year) to `data/cache/{id}_scout.json`.

## 3. Extractor Agent (The Regulatory Brain)
- [ ] 3.1 Create `workflows/sub_extractor.json`.
- [ ] 3.2 **Implement Binary Caching (The Vault)**:
    - Input: `pdf_url` from Scout.
    - Check if `data/cache/artifacts/{id}_{year}.pdf` exists.
    - **IF MISSING**: Use HTTP Request (Get Stream) to download and `Write Binary File` to disk.
    - **IF PRESENT**: Use `Read Binary File` to load from disk (Speed + Offline safety).
- [ ] 3.3 **Implement Text Caching**:
    - Check if `data/cache/{id}_raw_text.txt` exists.
    - If no, Parse the **Local PDF Binary** -> Save Text.
- [ ] 3.4 Implement **Financial Extraction** (LLM Node):
    - *System Prompt:* "You are a forensic accountant. Extract exact figures from the provided text..."
    - *Schema Mapping:* Map `total_income`, `program_expenses`, `lsg_reserve_amount`.
    - *Constraint:* STRICTLY ignore Cap 622/Director metrics.
- [ ] 3.5 Save structured data to `data/cache/{id}_extracted.json`.

## 4. Risk Agent (Reputation Check)
- [ ] 4.1 Create `workflows/sub_risk.json`.
- [ ] 4.2 **Implement Caching**: Check `data/cache/{id}_risk.json` before searching.
- [ ] 4.3 Implement Search API -> Sentiment Filter.
- [ ] 4.4 Save flags to `data/cache/{id}_risk.json`.

## 5. Orchestration & Merge
- [ ] 5.1 Update `workflows/main_orchestrator.json`.
- [ ] 5.2 Implement `Merge` node to load all 3 cache files.
- [ ] 5.3 Add `Write to File` node: Save combined result to `data/organisations/{uuid}.json`.