# Project Context

## Purpose
The CharityGrader project aims to democratize and automate philanthropic due diligence. It bridges the gap between unstructured public disclosures and rigorous, comparable metrics. By architecting an offline-sovereign auditing engine, we empower donors and stakeholders to evaluate non-profits based on **Financial Health**, **Regulatory Compliance** (specifically LSG Manual), and **Impact Evidence** (Effective Altruism principles). The system transforms ephemeral web data into immutable, schema-validated JSON artifacts, rendered into static, portable report cards.

## Tech Stack
* **Orchestration:** n8n (Self-hosted, Dockerized)
* **AI/Intelligence:** Perplexity API (Sonar)
* **Scripting:** Python 3.x (Pandas, PyPDF2) - embedded in n8n nodes
* **Data Persistence:** JSON (Filesystem-based), Git (Version Control)
* **Static Site Generator:** Hugo (Golang-based)
* **Styling:** Tailwind CSS (Utility-first)
* **Search:** Perplexity API

## Project Conventions

### Code Style
* **JSON Schema:** All data ingress/egress must validate against `governance.schema.json`. Use `snake_case` for all JSON keys.
* **Python:** Follow PEP 8. Functions must be pure where possible. Explicit type hinting required.
* **n8n:** Workflows must be modular. Error handling nodes are mandatory for external API calls.
* **Hugo/HTML:** Semantic HTML5. No inline styles. Accessibility (ARIA) compliance required.

### Architecture Patterns
* **OpenSpec Native:** No code without specs. Cycle: `Proposal -> Spec -> Tasks -> Implementation`.
* **Separation of Concerns:**
    * *Orchestrator (n8n):* Manages the data extraction and processing workflow.
    * *Intelligence (LLM):* Extracts unstructured data from documents into JSON.
    * *Validation Service (Python/FastAPI):* A microservice that ensures all extracted data conforms to centralized JSON schemas before persistence.
    * *Data Vault (PocketBase):* Stores validated JSON artifacts and source documents.
    * *Renderer (Hugo):* Visualizes the final data as static report cards.
* **Offline Sovereignty:** The final build must function without a backend, database, or internet connection.
* **Human-in-the-Loop:** Subjective AI judgments (e.g., "High Risk") are flagged for review via `warnings.log`, not auto-published.

### Testing Strategy
* **Schema Validation:** A dedicated validation microservice strictly enforces adherence to centralized JSON schemas for all data before it is persisted.
* **Logic Verification:** Unit tests for financial ratio calculations (e.g., Liquidity Ratio, Program Expense Ratio).
* **Build Integrity:** Hugo build fails if data templates encounter missing required fields.

### Git Workflow
* **Branching:** `main` is production/stable. `feature/capability-name` for active development.
* **Commits:** Conventional Commits (e.g., `feat: add liquidity logic`, `fix: scraper timeout`).

## Domain Context

### Effective Altruism (EA)
Prioritize **"Counterfactual Impact"** (what happened vs. what would have happened). Skepticism towards "overhead myths" but vigilance on "room for funding".

### Hong Kong Regulations
* **Lump Sum Grant (LSG) Manual:** Rules on reserve caps (25% of operating expenditure) and clawback mechanisms.

### Financial Metrics
* **Liquidity Ratio:** `(Net Assets - Restricted Funds) / Monthly Expenses`.
    * *Target:* > 3 months.
* **Program Expense Ratio:** `Program Expenses / Total Expenses`.
    * *Benchmark:* > 70-80%.

## Product Design: The Audit Checklist Model

### Core Logic
Instead of a single aggregate score, the system evaluates charities through a **Binary Audit Checklist**.
- **Check-Items:** Atomic validation functions (e.g., `check_reserve_cap`, `check_unmodified_audit`).
- **Results:** Each item returns a `pass` or `fail` status.
- **Metadata:** Each item includes:
    - `significance`: [HIGH | MEDIUM | LOW]
    - `details`: Narrative explaining the formula and data source snippets.
    - `category`: [Financial Health | Governance | Impact Awareness].

### UI Ranking & Display
- **Priority Sorting:** Failed items with 'HIGH' significance are bubbled to the top of the stack.
- **Transparency:** Every item is expandable to show the exact calculation (e.g., "$HKD X (Reserve) / $HKD Y (Expenses) = 28%").

### Implementation Strategy
- **Logic Layer (utils_api):** The Python validation service is expanded to include a registry of audit functions.
- **Data Persistence:** The `analytics` JSON field in PocketBase stores the array of check-item results.

## Important Constraints
* **No Hallucinations:** Extracted data must cite a `source_url` and `text_snippet`. If data is missing, return `null`; do not guess.
* **Offline First:** No external CDNs (Google Fonts, JSDelivr) in the final HTML. All assets must be bundled.
* **Privacy & Ethics:** Do not scrape or publish PII of beneficiaries. Only public governance data (Directors) is processed.
* **Rate Limiting:** Respect `robots.txt` and implement delay strategies in scrapers.

## External Dependencies
* **LLM Providers:** Perplexity (Extraction/Research/Search).
* **Search Engines:** Perplexity Search APIs (for finding Annual Reports).
* **Charity Registries:** HK CSS (Council of Social Service) directory (as a seed list).