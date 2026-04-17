## 1. Schema Updates (`schemas/`)
- [ ] 1.1 Open `schemas/v1/financials.schema.json`.
- [ ] 1.2 Locate the base definition for financial objects (or apply to `income`, `expenditure.total`, `expenditure.program_services`, and `reserves`).
- [ ] 1.3 Add a new integer property `"scale_multiplier"` with an enum constraint of `[1, 1000, 1000000]` and a default of `1`.

## 2. Prompt Engineering (`n8n/prompt-templates/`)
- [ ] 2.1 Open `n8n/prompt-templates/financials.system.md`.
- [ ] 2.2 Add an instruction under the strict extraction rules: "CRITICAL: Look carefully at table headers, column names, or footnotes for scale indicators like 'in thousands', 'in HK$ \'000', 'in millions', or 'mn'. If found, extract the number EXACTLY as written in the cell into the `value` field (do not manually add zeroes). Then, set the `scale_multiplier` field to `1000` or `1000000` accordingly. If no scale is indicated, set it to `1`."

## 3. Python Audit Engine (`utils_api/app/audits/`)
- [ ] 3.1 Open `utils_api/app/audits/impact.py`.
- [ ] 3.2 In the `check_cost_per_outcome` function, locate the extraction of program spend (e.g., `program_spend = record.financials.expenditure.program_services.value`).
- [ ] 3.3 Update the extraction to factor in the scale: `raw_spend = record.financials.expenditure.program_services.value` and `multiplier = record.financials.expenditure.program_services.scale_multiplier or 1`. 
- [ ] 3.4 Calculate the true local spend: `true_local_spend = raw_spend * multiplier`.
- [ ] 3.5 Pass `true_local_spend` into the existing `usd_exchange_rate` conversion logic. Ensure total expenditure calculations (if used elsewhere in the API) follow this same pattern.
- [ ] 3.6 Update `utils_api/tests/test_audit_impact.py` to include a mock record with a `value` of `20` and a `scale_multiplier` of `1000000`, asserting that the calculated USD cost scales correctly.

## 4. Hugo UI Updates (`web/`)
- [ ] 4.1 Open `web/layouts/partials/impact-pathway.html`.
- [ ] 4.2 Locate the Inputs card where `$financials.expenditure.total.value` is processed.
- [ ] 4.3 Add Hugo math to resolve the true local value: `{{ $multiplier := .scale_multiplier | default 1 }}` and `{{ $true_local := mul .value $multiplier }}`.
- [ ] 4.4 Update the USD math to use `$true_local`: `{{ $usd_total := mul $true_local $rate }}`.
- [ ] 4.5 Update the tooltip `title` attribute to explicitly declare the math for provenance: `title="Original: {{ $financials.currency.original_code }} {{ lang.FormatNumber 0 $true_local }} (Extracted as {{ .value }} x {{ $multiplier }}). Rate: {{ $rate }}"`.