## 1. Schema Updates (`schemas/`)
- [x] 1.1 Open `schemas/v1/impact.schema.json`. Update the `beneficiary_type` enum under the `beneficiaries` array to include `"unspecified"`.

## 2. Prompt Engineering (`n8n/prompt-templates/`)
- [ ] 2.1 Open `n8n/prompt-templates/impact.system.md`.
- [ ] 2.2 Add an instruction to Principle 2 (Conservative Extraction): "Only count actual, realized beneficiaries that were directly impacted during the reporting timeframe. Do NOT count potential, predicted, guessed, or indirect future beneficiaries."
- [ ] 2.3 Add an instruction to Principle 5 (Disaggregated Populations): "Do NOT classify animal products (e.g., eggs, meals served, pounds of meat) as animal beneficiaries."
- [ ] 2.4 Add an instruction to Principle 5 defining classification rules: "Classify dogs and cats as `companion_animals` even if they are strays or community animals. For other animals, rely on context (e.g., a pet pig is a `companion_animal`, an agricultural pig is `farmed_animals`). If the species is completely ambiguous or listed generically as 'others', use `unspecified`."

## 3. Python Audit Engine (`utils_api/app/audits/`)
- [ ] 3.1 Open `utils_api/app/audits/impact.py`.
- [ ] 3.2 In `check_cause_area_neglectedness`, update the `populations` dictionary to include: `"unspecified": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type == "unspecified" and b.population)`.
- [ ] 3.3 Ensure the `unspecified` key is accounted for in formatting logic (e.g., title-casing the breakdown string) so it renders correctly in the `AuditDetails` string if present.

## 4. Hugo UI Updates (`web/`)
- [ ] 4.1 Create a new SVG icon for the unspecified type: `web/layouts/partials/icons/unspecified-animals.svg` (e.g., a generic animal footprint or question mark).
- [ ] 4.2 Open `web/layouts/index.html`. In the Target Species column logic (around line 52), update the `$s.Set "popMap"` initialisation to include `"unspecified" 0.0` so it doesn't crash when iterating over the JSON array.
- [ ] 4.3 Open `web/layouts/partials/itn-scorecard.html`.
- [ ] 4.4 Update `$s.Set "popMap"` initialisation to include `"unspecified" 0.0`.
- [ ] 4.5 Update the `$iconMap` dictionary to include `"unspecified" "icons/unspecified-animals.svg"`.
- [ ] 4.6 Modify the rendering loop for `$sortedBeneficiaries`. Add a Hugo `if` condition to check if the current `.type` is `"unspecified"`. If it is `"unspecified"`, ensure it *only* renders if its `.pop` is `> 0`. For the other 3 types, retain the existing logic that renders them in grayscale when their `.pop` is `<= 0`.