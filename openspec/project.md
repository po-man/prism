# PRISM: An Audit Engine for Animal Advocacy Analytics

**P**awsitive **R**eporting & **I**mpact **S**u**m**mary (PRISM) is a data-driven evaluation platform for Hong Kong's animal advocacy sector. It provides objective, auditable insights into charities' effectiveness and risk, helping donors make more informed decisions.

---

## Part 1: Project Overview (Non-Technical)

### 1.1 The Problem
The Hong Kong animal advocacy sector is highly fragmented. While large, established organisations publish structured reports, dozens of high-impact, grassroots rescues lack the resources for formal reporting. This leads to a situation where donors often give based on emotional appeal or brand recognition, rather than on evidence-based principles of effectiveness and risk. There is no central, data-driven platform for evaluating these charities.

### 1.2 Our Solution
We are building a specialised analytics platform to evaluate Hong Kong animal non-profits. The system combines automated analysis of official documents (like annual reports) with intelligent web and news searches. It produces clear, confidence-weighted metrics on each charity's **Financials**, **Impact**, and **Risk**, with a special focus on prioritising underfunded cause areas (e.g., farm animal advocacy) in line with Effective Altruism (EA) principles.

### 1.3 How It Works: The Audit Checklist
Instead of creating a single, subjective "score", our system works like a deterministic audit engine. It processes information through two parallel tracks and evaluates it against a clear set of rules.

1.  **Track A: Document Analysis:** If a charity provides official documents (like an Annual Report or Audited Financials), the system uses AI to extract key data: total income, program expenses, and quantified impact (e.g., "500 animals rescued").
2.  **Track B: Public Risk Search:** For every charity, the system searches the web and news archives for keywords like "scandal," "investigation," or "abuse" to flag any potential reputational or regulatory issues.

The data from both tracks is then fed into an **Audit Engine**, which runs a series of checks. The final output is a simple, easy-to-understand checklist for each organisation, with each item marked as Pass (🟢), Warning (🟡), Fail (🔴), or Not Available (⚪).

---

## Part 2: Technical Specification

### 2.1 Tech Stack
* **Orchestration:** n8n (self-hosted)
* **AI/Intelligence:** Google Gemini API (for extraction and research)
* **PDF Processing:** Stirling PDF API (self-hosted)
* **Scripting:** JavaScript/Python
* **Data Persistence:**
    *   **Primary:** PocketBase (self-hosted, for storing all validated data artifacts and source documents).
    *   **Secondary:** Filesystem JSON (as the data source for the static site generator).
* **Static Site Generator:** Hugo (Golang-based)
* **Styling:** Tailwind CSS (Utility-first)

### 2.2 Architecture & Workflow
* **OpenSpec Native:** No code without specs. Cycle: `Proposal -> Spec -> Tasks -> Implementation`.
* **Separation of Concerns:**
    * *Orchestrator (n8n):* Manages the entire data pipeline, from ingestion to persistence.
    * *Intelligence (Gemini):* Extracts unstructured data from documents and web searches into structured JSON.
    * *PDF Service (Stirling):* Handles flattening and compression of PDF documents.
    * *Utils Service (Python/FastAPI):* A microservice that ensures all extracted data conforms to centralised JSON schemas before persistence; and handle audit analysis logic.
    * *Data Vault (PocketBase):* The single source of truth for validated JSON artifacts and source documents.
    * *Renderer (Hugo):* Visualizes the final data as static report cards.
* **Offline Sovereignty:** The final build (static website) must function without a backend, database, or internet connection.

#### Workflow Phases
1.  **Initialization:** The workflow is triggered with a payload containing the organization's names, cause area, and an array of official document URLs.
2.  **Parallel Extraction:**
    *   **Track A (Document Parsing):** If `document_urls` is not empty, n8n calls the Stirling PDF API to OCR the documents. The docuemnts are then passed to the Gemini API with a specific prompt to extract financial and impact data into a structured JSON object.
    *   **Track B (Risk Search):** The Gemini API's web search function is used to query for negative news or incidents related to the organization.
3.  **Audit Engine:** The merged data from both tracks is passed to the `utils_api` (Python/FastAPI service). This service runs a series of predefined audit functions against the data.
4.  **Persistence & Output:** The `utils_api` returns an `analytics` object containing the `check_items` array. This object is validated against its schema and then saved to the organization's record in PocketBase. Finally, the data is exported as a JSON file for Hugo to consume.

### 2.3 Project Conventions
*   **Code Style:**
    *   **JSON Schema:** All data must validate against a corresponding schema (e.g., `financials.schema.json`). Use `snake_case` for all JSON keys.
    *   **JavaScript (n8n):** Use modern ES6+ syntax. Functions should be pure where possible. Add JSDoc comments for complex logic.
    *   **n8n:** Workflows must be modular. Use sub-workflows for reusable logic (e.g., "Prompt Injection"). Error handling nodes are mandatory for all external API calls.
    *   **Hugo/HTML:** Use semantic HTML5. No inline styles. Prioritize accessibility (ARIA).
*   **Git Workflow:**
    *   **Branching:** `main` is production/stable. Use `feature/capability-name` for active development.
    *   **Commits:** Adhere to Conventional Commits standard (e.g., `feat: add cause_area_neglectedness check`, `fix: handle empty document_urls array`).

### 2.4 Domain Context & Audit Logic
The core evaluation framework is based on Effective Altruism (EA) principles applied to animal advocacy.

*   **Effective Altruism (EA):** We prioritize interventions based on **Importance, Tractability, and Neglectedness (ITN)**.
    *   **Neglectedness:** Cause areas like "Farm" and "Wildlife" are considered higher impact than the highly saturated "Companion" animal space in Hong Kong.
    *   **Tractability:** We look for evidence of quantified impact (e.g., cost-per-animal-rescued) over purely anecdotal claims.
*   **Financial Health Metrics:**
    *   **Program Expense Ratio:** `Program Expenses / Total Expenses`. A common benchmark is, says, > 65%.
*   **Audit Checklist Model:**
    *   **Logic Layer (`utils_api`):** The Python validation service is expanded to include a registry of audit functions (e.g., `check_financial_disclosure`, `check_cause_area_neglectedness`).
    *   **Data Persistence:** The `analytics` JSON field in the `organisations` collection in PocketBase stores the array of check-item results.
    *   **Example Check Item:**
        ```json
        {
          "category": "EA Impact Alignment",
          "id": "check_cause_area_neglectedness",
          "status": "pass",
          "details": {
            "calculation": "Target operates in Farm Animal Advocacy, which is highly neglected in HK."
          }
        }
        ```

### 2.5 Testing Strategy
*   **Schema Validation:** A dedicated `utils_api` endpoint (`/validate`) strictly enforces adherence to centralised JSON schemas for all data before it is persisted in PocketBase.
*   **Logic Verification:** Unit tests for the audit functions within the `utils_api` (e.g., `check_program_expense_ratio`).
*   **Build Integrity:** The Hugo build will fail if its data templates encounter missing required fields in the input JSON, ensuring data consistency.

### 2.6 Important Constraints
*   **No Hallucinations:** Extracted data from the LLM must be verifiable. The prompt requires citing a `source_url` and `text_snippet` where possible. If data is missing from a source document, the LLM must return `null`, not invent a value.
*   **Offline First:** The final rendered HTML reports must not rely on external CDNs (e.g., Google Fonts, JSDelivr). All assets must be bundled with the Hugo build.
*   **Privacy & Ethics:** Do not scrape or publish Personally Identifiable Information (PII) of beneficiaries. Only publicly available governance data (e.g., names of directors) is processed.
*   **Rate Limiting:** API calls in n8n must respect provider rate limits. Implement exponential backoff or delays in retry-on-fail nodes.