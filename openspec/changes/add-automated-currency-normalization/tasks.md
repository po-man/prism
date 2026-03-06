# openspec/changes/add-automated-currency-normalization/tasks.md

## 1. Schema & Prompt Updates (`schemas`, `n8n`)
- [x] 1.1 In `schemas/v1/financials.schema.json`, add the `currency` object at the root level, requiring `original_code`, `usd_exchange_rate`, and `rate_date`. 
- [x] 1.2 In `n8n/prompt-templates/financials.system.md`, append an instruction: "Identify the primary currency used in the financial report. Output its 3-letter ISO 4217 code (e.g., USD, HKD, INR, SGD) in the `currency.original_code` field."

## 2. Orchestrator Logic (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 2.1 Insert a Code Node immediately after "Parsed Content (Financials)". 
    - Write JS logic to extract the base year from `$json.parsedContentObject.financial_year` (e.g., `const year = fy.match(/^\d{4}/)[0];`).
    - Define the target date: `const targetDate = `${year}-12-31`;`.
    - Check if the code is 'USD'. If true, set rate to `1.0` and skip API.
- [ ] 2.2 Insert an HTTP Request Node to call `https://api.frankfurter.dev/v1/{{ $json.targetDate }}?base={{ $json.original_code }}&symbols=USD`.
- [ ] 2.3 Insert a Code Node to map the response back into the main payload, setting `usd_exchange_rate = response.rates.USD` and `rate_date = response.date`.
- [ ] 2.4 Re-link the pipeline to pass this enriched payload into the `Schema Validation (Financials)` node.

## 3. Python Audit Engine (`utils_api`)
- [ ] 3.1 In `utils_api/app/audits/impact.py` -> `calculate_cost_per_outcome`:
    - Fetch the rate: `rate = record.financials.currency.usd_exchange_rate if record.financials.currency and record.financials.currency.usd_exchange_rate else 1.0`.
    - Apply the rate: `program_spend_usd = program_spend * rate`.
    - Update all math and f-strings to explicitly use `program_spend_usd` and state "USD".
- [ ] 3.2 In `utils_api/tests/test_audit_impact.py`, update `VALID_BASE_RECORD` to include the new `currency` object, and adjust expected test outputs to look for the USD formatting.

## 4. UI / Hugo Refactoring (`web`)
- [ ] 4.1 In `web/layouts/index.html` (Master Table):
    - Change the table header from `<th ...>Cost per Outcome (HKD)</th>` to `Cost per Outcome (USD)`. 
    - In the corresponding `<td>`, wrap the output in a `span` with a tooltip that pulls the detailed calculation string (which contains the original local currency math): `<span title="{{ $cost_metric.details.calculation }}">USD ${{ printf "%.2f" $cost_metric.value }}</span>`.
- [ ] 4.2 In `web/layouts/partials/impact-pathway.html` (Inputs Card):
    - Locate the `with $financials.expenditure.total` block. 
    - Add Hugo math: `{{ $rate := $financials.currency.usd_exchange_rate | default 1.0 }}` and `{{ $usd_total := mul . $rate }}`.
    - Change display to: `USD ${{ lang.FormatNumber 0 $usd_total }}`.
    - Add tooltip to the number: `title="Original: {{ $financials.currency.original_code }} {{ lang.FormatNumber 0 . }} (Rate: {{ $rate }})"`.
- [ ] 4.3 In `web/layouts/partials/myth-buster.html` (Value for Money):
    - Update the header to "Estimated Cost per Outcome (USD)". 
    - The extracted `$cost_per_outcome_raw` (which maps to `details.calculation`) will now be provided in USD by the `utils_api`, but update the HTML to ensure the raw calculation string is fully visible or available as a tooltip on the final USD figure.
    - For the "Expense Breakdown" progress bar, add the local currency to the existing tooltips: `title="Program: {{ $financials.currency.original_code }} {{ lang.FormatNumber 0 $prog_exp }} ({{ lang.FormatNumber 1 $prog_pct }}%)"`.