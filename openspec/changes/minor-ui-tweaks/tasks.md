## 1. Favicon Integration (`web/layouts/_default/baseof.html`)
- [ ] 1.1 In the `<head>` section, add a favicon link: `<link rel="icon" type="image/x-icon" href="{{ "favicon.ico" | relURL }}">`.
- [ ] 1.2 Add a placeholder `favicon.ico` file to the `web/static/` directory (you will need to provide the actual icon file here).

## 2. Financial Year Display
- [ ] 2.1 In `web/layouts/_default/single.html`, locate the header section under the `registration_id`.
- [ ] 2.2 Add a conditional block to display the financial year:
  ```html
  {{ with $org.financials.data.financial_year }}
    <p class="mt-1 text-sm text-gray-500 font-mono">FY: {{ . }}</p>
  {{ end }}
  ```
- [ ] 2.3 In `web/layouts/partials/impact-pathway.html`, locate the `<p class="text-gray-600">Total Annual Expenditure</p>` line.
- [ ] 2.4 Update it to include the financial year context:
  ```html
  <p class="text-gray-600">Total Annual Expenditure {{ with $financials.financial_year }}(FY {{ . }}){{ end }}</p>
  ```

## 3. Data Source Icon Spacing (`web/layouts/_default/single.html`)
- [ ] 3.1 Locate the "Data Sources:" block (around line 34).
- [ ] 3.2 Change all instances of `<span class="ml-1.5">` to `<span class="ml-0.5">` next to the SVG partials for "Annual Report", "Financials", and "Web Search".

## 4. Timezone Localisation (Hong Kong Time)
- [ ] 4.1 In `web/layouts/_default/single.html`, locate the "Last Updated" format: `{{ dateFormat "Jan 2, 2006" . }}`.
- [ ] 4.2 Replace it with timezone-aware logic: 
  `{{ (. | time.AsTime).In (time.LoadLocation "Asia/Hong_Kong") | time.Format "Jan 2, 2006" }}`
- [ ] 4.3 In `web/layouts/index.html`, locate the `data-sort-value` timestamp parsing: `{{ with $org.updated }}{{ dateFormat "2006-01-02" . }}{{ else }}0{{ end }}`.
- [ ] 4.4 Replace it with: `{{ with $org.updated }}{{ (. | time.AsTime).In (time.LoadLocation "Asia/Hong_Kong") | time.Format "2006-01-02" }}{{ else }}0{{ end }}`.
- [ ] 4.5 In `web/layouts/index.html`, locate the visual table cell timestamp parsing: `{{ dateFormat "2006/01/02" . }}`.
- [ ] 4.6 Replace it with: `{{ (. | time.AsTime).In (time.LoadLocation "Asia/Hong_Kong") | time.Format "2006/01/02" }}`.

## 5. Table Sorting Inversion (`web/layouts/index.html`)
- [ ] 5.1 In the `<thead>` section of the `#audits-table`, change every instance of `data-sort-dir="asc"` to `data-sort-dir="desc"`. This ensures the JavaScript will treat the first click as a trigger for a descending sort.