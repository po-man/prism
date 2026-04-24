## 1. Jargon & "Annual" Badge Removal (`web/layouts/`)i
- [x] 1.1 In `web/layouts/index.html`, locate the table headers (`<thead>`). Remove ` (Neglectedness)` from the Target Species column and ` (Importance)` from the Total Beneficiaries column. Also, update the corresponding `data-label` attributes in the `<tbody>` rows.
- [x] 1.2 In `web/layouts/partials/index-how-to-read.html`, update the `data-highlight-column` attributes and the `<h4>` elements to match the new simplified header names ("Target Species" and "Total Beneficiaries").
- [x] 1.3 In `web/layouts/partials/itn-scorecard.html`, locate and delete the two `<span class="text-[10px] font-mono... >Annual</span>` badges (under "Scale of Reach" and "Beneficiary Demographics").
- [x] 1.4 In `web/layouts/partials/ies-scorecard.html`, locate and delete the `<span class="inline-flex items-center... >Annual</span>` badge next to the main header.

## 2. Master Table Unspecified Icon (`web/layouts/index.html`)
- [x] 2.1 In `web/layouts/index.html`, locate the `<td data-label="Target Species">` block within the range loop.
- [x] 2.2 Add the Hugo math and rendering logic for the `unspecified` beneficiary type, mirroring the existing logic used for farmed, wild, and companion animals. 
    - Extract `$unspecified_pop`.
    - Calculate `$unspecified_pct_raw` and `$unspecified_pct_rounded`.
    - Set `$unspecified_opacity`.
    - Render `partial "icons/unspecified-animals.svg"` wrapped in a `tooltip.html` partial, applying the `grayscale` class if the population is `<= 0`.

## 3. Intervention Portfolio Badges & Key (`web/layouts/partials/itn-scorecard.html`)
- [x] 3.1 Refactor the `$interventionMap` scratchpad logic inside the Tractability card. 
    - Instead of just appending sources, map the intervention name to a dictionary containing both the sources and a dynamic CSS class based on `.tier_name`.
    - Implement conditional logic: If `.tier_name` contains "Tier 1", class is `bg-purple-100 text-purple-800`. If "Tier 2", class is `bg-blue-100 text-blue-800`. Else (Tier 3), class is `bg-gray-100 text-gray-800`.
- [x] 3.2 Update the badge rendering loop (`{{ range $name, $data := $interventionMap.Values }}`) to apply `{{ $data.class }}` to the badge wrapper `<div>`, and iterate over `first 3 $data.sources`.
- [x] 3.3 Add the legend HTML block immediately below the flex container of badges:
  ```html
  <div class="mt-4 text-xs text-gray-500 italic">
    <p><span class="font-bold text-purple-800">Purple values</span> represent Tier 1 (Systemic Change) interventions.</p>
    <p><span class="font-bold text-blue-800">Blue values</span> represent Tier 2 (Prevention & Scalable Care) interventions.</p>
    <p><span class="font-bold text-gray-800">Grey values</span> represent Tier 3 (Direct Care & Indirect Action) interventions.</p>
  </div>
  ```