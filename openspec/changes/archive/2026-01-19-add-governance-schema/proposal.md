# Proposal: Governance Data Schema

## Why
To enable automated auditing via LLMs without risking "hallucinations," we must define a strict JSON contract. This schema serves as the system's "Constitution," translating specific Hong Kong statutory laws (Cap. 622) and LSG financial rules into validating code. It focuses on objective data extractable from official Annual Reports.

## What Changes
- **New Capability:** `data-schemas`
- **Schema Definition:** Creation of `schemas/governance.schema.json` with strict validation for:
  - **Financials:** Automatic ratio calculation logic (Liquidity, Program Expense).
  - **LSG Compliance:** Specific checks for Reserve caps (25% rule).
  - **Impact (Internal):** Stated beneficiary counts and Evidence Quality (Self-reported).
- **Traceability:** A universal `SourceTraceability` pattern requiring every metric to cite a specific URL and text snippet.

## Impact
- **n8n Workflows:** Structured Output Parsers must now strictly adhere to this schema.
- **Web Layer:** Hugo templates will rely on these specific keys for rendering "Traffic Light" status indicators.