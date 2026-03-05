# PRISM: An Audit Engine for Animal Advocacy Analytics

**P**awsitive **R**eporting & **I**mpact **S**u**m**mary (PRISM) is a data-driven evaluation platform for the animal advocacy sector. It provides objective, auditable insights into charities' effectiveness, helping donors make more informed decisions.

---

## Part 1: Project Overview (Non-Technical)

### 1.1 The Problem
The animal advocacy sector, particularly in Asia, is highly fragmented. While large, established organisations publish structured reports, dozens of high-impact, grassroots rescues lack the resources for formal reporting. This leads to a situation where donors often give based on emotional appeal or brand recognition, rather than on evidence-based principles of effectiveness. There is no central, data-driven platform for evaluating these charities.

### 1.2 Our Solution
We are building a specialised analytics platform to evaluate animal non-profits globally. The system combines automated analysis of official documents (like annual reports) with intelligent web research. It produces clear, confidence-weighted metrics on each charity's **Financials** and **Impact**, with a special focus on prioritising underfunded cause areas (e.g., farm animal and wild animal advocacy) in line with Effective Altruism (EA) principles.

### 1.3 How It Works: The Audit Checklist
Instead of creating a single, subjective "score", our system works like a deterministic audit engine. It processes information through two parallel tracks and evaluates it against a clear set of rules.

1.  **Track A: Document Analysis:** If a charity provides official documents (like an Annual Report or Audited Financials), the system uses AI to extract key data: total income, program expenses, and quantified impact (e.g., "500 animals rescued").
2.  **Track B: Web Impact Search:** To bridge the data gap for grassroots organisations, the system actively searches the web for impact-related snippets, beneficiary demographics, and significant events associated with the charity's official domains.

The data from both tracks is merged, citations are resolved to exact text-fragments, and the payload is fed into an **Audit Engine**. The final output is an easy-to-understand report card for each organisation, with each checklist item marked as Pass (🟢), Warning (🟡), Fail (🔴).

---

## Part 2: Technical Specification

### 2.1 Tech Stack
* **Orchestration:** n8n (self-hosted)
* **AI/Intelligence:** Google Gemini API (for extraction, grounding, and research)
* **PDF Processing:** Stirling PDF API (self-hosted)
* **Scripting / Logic:** Python/FastAPI (`utils_api`)
* **Data Persistence:**
    * **Primary:** PocketBase (self-hosted, for storing all validated data artifacts and source documents).
    * **Secondary:** Filesystem JSON (as the data source for the static site generator).
* **Static Site Generator:** Hugo (Golang-based)
* **Styling:** Tailwind CSS (Utility-first)
* **CI/CD:** GitHub Actions (Automated build and deployment to GitHub Pages)

### 2.2 Architecture & Workflow
* **OpenSpec Native:** No code without specs. Cycle: `Proposal -> Spec -> Tasks -> Implementation`.
* **Separation of Concerns:**
    * *Orchestrator (n8n):* Manages the entire data pipeline, from ingestion to persistence.
    * *Intelligence (Gemini):* Extracts unstructured data from documents and web searches into structured JSON.
    * *PDF Service (Stirling):* Handles flattening and compression of PDF documents.
    * *Utils Service (Python/FastAPI):* A microservice that ensures all extracted data conforms to centralised JSON schemas, resolves redirecting URLs, and executes deterministic audit logic.
    * *Data Vault (PocketBase):* The single source of truth for validated JSON artifacts and source documents.
    * *Renderer (Hugo):* Visualises the final data as static report cards.
* **Offline Sovereignty:** The final build (static website) functions without a backend, database, or runtime API connection. 

#### Workflow Phases
1.  **Initialisation:** The workflow is triggered with a payload containing the organisation's name, batch ID, and official document URLs.
2.  **Parallel Extraction:**
    * **Track A (Document Parsing):** n8n calls the Stirling PDF API to OCR the documents. The documents are passed to the Gemini API to extract financial data.
    * **Track B (Impact Search & Fusion):** The Gemini API searches the web for impact snippets. Both web snippets and PDF text are fed to Gemini to extract a unified, deduplicated impact schema.
3.  **Audit Engine:** The merged data is passed to the `utils_api`. This service runs predefined audit functions (e.g., threshold checks, cost-per-outcome calculations).
4.  **Persistence & Output:** The data is validated against strict schemas, saved to PocketBase, and exported as `[id].json` and markdown stubs for Hugo.
5.  **Deployment:** Merging the data vault to the release branch and tagging a release (`vYYYY.MM.DD`) triggers a GitHub Action to build the Hugo site and deploy it to GitHub Pages.

### 2.3 Project Conventions
* **Code Style:**
    * **JSON Schema:** All data must validate against a corresponding schema (e.g., `financials.schema.json`). Use `snake_case` for all JSON keys.
    * **JavaScript (n8n):** Use modern ES6+ syntax. Functions should be pure where possible. 
    * **n8n:** Workflows must be modular. Error handling nodes are mandatory for all external API calls.
    * **Hugo/HTML:** Use semantic HTML5. Prioritise accessibility (ARIA).
* **Git Workflow:**
    * **Versioning:** Calendar Versioning (CalVer), e.g., `v2026.03.05`.
    * **Commits:** Adhere to Conventional Commits standard (e.g., `feat: add cause_area_neglectedness check`).

### 2.4 Domain Context & Audit Logic
The core evaluation framework is based on Effective Altruism (EA) principles applied to animal advocacy.

* **Effective Altruism (EA):** We prioritise interventions based on **Importance, Tractability, and Neglectedness (ITN)**.
    * **Neglectedness:** Cause areas like "Farm" and "Wildlife" are considered higher impact than the highly saturated "Companion" animal space.
    * **Tractability:** We look for evidence of quantified impact (e.g., highest evidence quality found) over purely anecdotal claims.
* **Financial Health Metrics:**
    * **Liquidity & Reserves:** Checks for healthy operational runways without excessive hoarding.
    * **Cost Per Outcome:** Translated into a retail donor equivalent (e.g., "What a $1,000 donation achieves").
* **Audit Checklist Model:**
    * **Logic Layer (`utils_api`):** The Python validation service includes a registry of audit functions. Calculations are decoupled from strict Pass/Warn/Fail compliance thresholds.

### 2.5 Testing Strategy
* **Schema Validation:** A dedicated `utils_api` endpoint (`/validate`) strictly enforces adherence to centralised JSON schemas for all data before it is persisted.
* **Logic Verification:** Unit tests for the audit functions within the `utils_api` (e.g., `test_audit_impact.py`).
* **Build Integrity:** The Hugo build fails if data templates encounter missing required fields, ensuring complete data consistency before deployment.

### 2.6 Important Constraints
* **No Hallucinations:** Extracted data from the LLM must be verifiable. The prompt requires extracting exact, verbatim sentences (`source_quote`, `evidence_quote`). If data is missing from a source document, the LLM must return `null`.
* **Text-Fragment Verification:** Web-sourced claims are automatically deep-linked using W3C Text Fragments (`#:~:text=`), allowing users to click a metric and instantly see the claim highlighted on the charity's live website.
* **Offline First:** The final rendered HTML reports must not rely on external CDNs (e.g., Google Fonts, JSDelivr). All assets are bundled with the Hugo build.
* **Privacy & Ethics:** Do not scrape or publish Personally Identifiable Information (PII) of beneficiaries.