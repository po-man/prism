## 1. Schema Architecture (JSON Draft 7)
- [x] 1.1 Scaffold `schemas/governance.schema.json` with top-level objects: `meta`, `financials`, `governance`, `impact`, `audit_trail`.
- [x] 1.2 Define the reusable `definitions/source_ref` object containing `url` (uri-format), `fetched_at` (date-time), and `snippet` (string).

## 2. Financial Logic Implementation
- [x] 2.1 Define `financials.income` and `financials.expenditure` objects (all values must be `number`, minimum 0).
- [x] 2.2 Implement specific LSG fields: `lsg_reserve_amount`, `provident_fund_reserve`.
- [x] 2.3 Add `ratio_inputs` object: `net_current_assets`, `monthly_operating_expenses` to support Liquidity Ratio calculation.

## 3. Governance & LSG Logic
- [x] 3.1 Define `board_structure`: `size` (int), `independent_directors_count` (int), `remuneration_disclosed` (boolean).
- [x] 3.2 Implement LSG specific flags:
    - `is_lsg_compliant` (Boolean: Checks if reserves < 25% of operating exp).

## 4. Impact: Evidence & Scale (Reported)
- [x] 4.1 Define `impact.scale`: `beneficiaries_count` (int), `geographic_scope` (enum: HK-Wide, District, International).
- [x] 4.2 Define `impact.evidence_quality` Enum: `["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]`.
- [x] 4.3 Define `impact.transparency`: `reports_publicly_available` (boolean).

## 5. Validation & Testing
- [ ] 5.1 Create `tests/validate_schema.py` using the `jsonschema` library.
- [ ] 5.2 Create `data/mocks/pass_full_compliance.json` (Perfect NGO).
- [ ] 5.3 Create `data/mocks/fail_lsg_reserve.json` (Reserve > 25% violation).