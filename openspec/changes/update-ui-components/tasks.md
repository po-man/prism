## 1. Expense Breakdown Fallback (`web/layouts/partials/myth-buster.html`)
- [x] 1.1 Open `web/layouts/partials/myth-buster.html`.
- [x] 1.2 Locate the `{{ if ne $total_exp nil }}` block that wraps the "Expense Breakdown" card (Left Column).
- [x] 1.3 Move the `{{ if ne $total_exp nil }}` condition *inside* the main `<div class="p-4 bg-white rounded-lg shadow flex flex-col">` container so the card background always renders.
- [x] 1.4 Add an `{{ else }}` branch to this condition. Inside the `else` branch, implement a missing data fallback UI using the `icons/missing-ingredients.svg` and standard grey placeholder text (e.g., "Insufficient financial data to compute expense breakdown."), matching the layout of the missing Cost per Outcome state.

## 2. Proportional Audit Summary Opacity (`web/layouts/index.html`)
- [x] 2.1 Open `web/layouts/index.html`.
- [x] 2.2 Locate the "Audit Summary" `<td>` rendering block (around line 170).
- [x] 2.3 Calculate the total number of audits: `{{ $total_audits := add (add $pass $warn) $fail }}`.
- [x] 2.4 Within the `<span>` tags for the pass, warn, and fail indicators, calculate their respective opacities. Use Hugo math: `{{ $pass_opac := 0.2 }}{{ if gt $total_audits 0 }}{{ $pass_opac = add 0.2 (mul (div (float $pass) $total_audits) 0.8) }}{{ end }}` (repeat for `$warn_opac` and `$fail_opac`).
- [x] 2.5 Apply the calculated opacities as inline styles to the respective badge indicator spans (e.g., `<span class="..." style="opacity: {{ $pass_opac }};">...</span>`).

## 3. Intervention Portfolio Badge Capping (`web/layouts/partials/itn-scorecard.html`)
- [x] 3.1 Open `web/layouts/partials/itn-scorecard.html`.
- [x] 3.2 Locate the "Intervention Portfolio" rendering block (around line 125).
- [x] 3.3 Find the loop iterating over the provenance badges: `{{ range $sources }}`.
- [x] 3.4 Update the loop to strictly limit the output to the first three sources: `{{ range first 3 $sources }}`.