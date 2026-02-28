## 1. Prompt Engineering (`n8n`)
- [x] 1.1 Edit `n8n/prompt-templates/impact.system.md` to add an instruction: "When extracting the `beneficiaries` array, you must disaggregate the exact `population` count for each specific `beneficiary_type` whenever a charity serves multiple categories of animals. Do not combine them into a single entry if distinct numbers are available."

## 2. Python Audit Engine (`utils_api`)
- [x] 2.1 Refactor `check_cause_area_neglectedness` in `utils_api/app/audits/impact.py`.
    - Extract all beneficiaries.
    - Check if any beneficiary has a valid, non-zero `population`.
    - **If population data exists:** Sum total population. Calculate the percentage of `farmed_animals` + `wild_animals`. Apply scoring: `>= 50%` = `pass`, `> 0% and < 50%` = `warning`, `0%` = `warning`. Update the `details.calculation` string to explicitly state the percentage breakdown (e.g., "Operates primarily in low-neglectedness areas (Companion: 85%, Wild: 15%).").
    - **If population data is null:** Fall back to presence-based logic (if farmed/wild in types -> `pass`, else `warning`).
- [x] 2.2 Update `utils_api/tests/test_audit_impact.py` to cover the new mathematical logic:
    - Test case: Mixed portfolio where Farmed/Wild >= 50% (yields `pass`).
    - Test case: Mixed portfolio where Farmed/Wild < 50% (yields `warning`).
    - Test case: Missing `population` data (falls back to existing presence checks).

## 3. UI/UX Refactoring (`web`)
- [x] 3.1 Update `web/layouts/partials/itn-scorecard.html`.
    - Create Hugo Scratch variables to sum the total population (`$totalPop`) and the individual populations (`$companionPop`, `$farmedPop`, `$wildPop`) while iterating over `.impact.data.beneficiaries`.
    - Within the rendering loop for the beneficiary badges, evaluate if `$totalPop > 0`.
    - If true, calculate the percentage `div (mul $typePop 100.0) $totalPop` and format it using `lang.FormatNumber 0`.
    - Append the percentage to the UI label (e.g., `Companion Animals ({{ $pct }}%)`).
    - Ensure styling accurately applies the `opacity-40 grayscale` class to any type where `$typePop == 0` (or if it is entirely absent from the array).