## 1. Favicon Integration (`web/layouts/_default/baseof.html`, `web/assets/favicon/`)
- [x] 1.1 In `web/layouts/_default/baseof.html`, add `<link>` tags to the `<head>` to reference all favicon assets (`.svg`, `.png`, `.ico`, `apple-touch-icon.png`) from the `assets/favicon/` directory using Hugo's `resources.Get`.
- [x] 1.2 Update `web/assets/favicon/site.webmanifest` to be a Hugo template, using `resources.Get` to dynamically generate relative paths for the manifest icons.
- [x] 1.3 In `web/layouts/_default/baseof.html`, update the manifest link to process it as a template using `resources.ExecuteAsTemplate`, ensuring it works in non-root deployments.

## 2. Financial Year Display
- [x] 2.1 In `web/layouts/_default/single.html`, locate the header section under the `registration_id`.
- [x] 2.2 Add a conditional block to display the financial year:
  ```html
  {{ with $org.financials.data.financial_year }}
    <p class="mt-1 text-sm text-gray-500 font-mono">FY: {{ . }}</p>
  {{ end }}
  ```
- [x] 2.3 In `web/layouts/partials/impact-pathway.html`, locate the `<p class="text-gray-600">Total Annual Expenditure</p>` line.
- [x] 2.4 Update it to include the financial year context:
  ```html
  <p class="text-gray-600">Total Annual Expenditure {{ with $financials.financial_year }}(FY {{ . }}){{ end }}</p>
  ```

## 3. Data Source Icon Spacing (`web/layouts/_default/single.html`)
- [x] 3.1 Locate the "Data Sources:" block (around line 34).
- [x] 3.2 Change all instances of `<span class="ml-1.5">` to `<span class="ml-0.5">` next to the SVG partials for "Annual Report", "Financials", and "Web Search".

## 4. Table Sorting Inversion (`web/layouts/index.html`)
- [ ] 4.1 In the `<thead>` section of the `#audits-table`, change every instance of `data-sort-dir="asc"` to `data-sort-dir="desc"`. This ensures the JavaScript will treat the first click as a trigger for a descending sort.