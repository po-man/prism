## 1. n8n Orchestration Updates (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 1.1 In the "Prepare Markdown Stub" code node, remove `type: "audits"` from the `markdownStub` template string so it defaults to the standard page type.
- [ ] 1.2 In the "Write to web/content/audits/{id}.md" node, update the `fileName` parameter path from `=/home/node/.n8n-files/web/content/audits/{{...}}.md` to `=/home/node/.n8n-files/web/content/{{...}}.md`. Rename the node accordingly.

## 2. Hugo Routing & File Structure (`web/layouts`)
- [ ] 2.1 Rename the file `web/layouts/audits/list.html` to `web/layouts/index.html`.
- [ ] 2.2 Rename the file `web/layouts/audits/single.html` to `web/layouts/_default/single.html`.
- [ ] 2.3 Delete the now-empty `web/layouts/audits/` directory.
- [ ] 2.4 In `web/layouts/_default/single.html`, update the "Back to Directory" link from `<a href="/audits/"...` to `<a href="/"...`.

## 3. UI Updates: Master Table (`web/layouts/index.html`)
- [ ] 3.1 **Data Sources Column:**
  - Add `<th ...>Data Sources</th>` to the table head.
  - Inside the `{{ range .Pages }}` loop, add a new `<td>` for Data Sources.
  - Copy the logic from `single.html` that resolves `$has_web_source`, `$annual_report_url`, and `$financial_report_url`. 
  - Render the three SVGs in a row (`flex space-x-2`), applying `opacity-40 grayscale` to missing sources. Add `data-sort-value` to the `<td>` representing the count of available sources to allow column sorting.
- [ ] 3.2 **Target Species (Neglectedness) Column:**
  - Update the existing Target Species `<td>` to utilize a data-sort-value (e.g., scoring high neglectedness > low neglectedness so it sorts cleanly).
  - Re-implement the beneficiary loop logic from `itn-scorecard.html` inside this cell: calculate `$totalPop` and the `$popMap` dict.
  - Render the three species SVGs (Companion, Farmed, Wild) side-by-side.
  - For each SVG, calculate the percentage (`$pct_raw`). Use inline styles `style="opacity: {{ if gt $pct_raw 0 }}{{ math.Max 0.2 (div $pct_raw 100.0) }}{{ else }}0.2{{ end }};"` and apply a `grayscale` class if the value is 0. Add `title` attributes indicating the exact percentage on hover.
- [ ] 3.3 **Sorting Script Adjustments:**
  - Ensure the vanilla JS table sorting script in `index.html` correctly reads `data-sort-value` for the new icon-heavy columns, overriding the `innerText` parsing.

## 4. Cleanup & Rebuild
- [ ] 4.1 Delete any existing markdown files inside `web/content/audits/` to prevent old routes from lingering.
- [ ] 4.2 Re-trigger the n8n pipeline for your dataset to generate the new markdown stubs directly in `web/content/`.
- [ ] 4.3 Verify the Hugo build generates the master table at `/` and the organization profiles at `/<slug>`.