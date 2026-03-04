## 1. n8n Orchestration Updates (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [x] 1.1 Duplicate the "Write to data/organisations/{id}.json" node.
- [x] 1.2 Configure the new node to write a Markdown stub to `/home/node/.n8n-files/data/content/audits/{{ $('Storage API - Update Charity - Analytics').first().json.id }}.md`.
- [x] 1.3 Set the content of this file to include Hugo frontmatter:
  ```yaml
  ---
  title: "{{ $('Storage API - Update Charity - Analytics').first().json.name }}"
  data_id: "{{ $('Storage API - Update Charity - Analytics').first().json.id }}"
  type: "audits"
  ---
  ```
  *(Note: You will need to map `content/` as a volume in docker-compose if it isn't already, or write directly to the Hugo content folder).*

## 2. Branding Updates (`web`)
- [ ] 2.1 In `web/layouts/_default/single.html` and any other layout files, replace `<h1 class="text-4xl font-bold text-blue-700">CharityGrader</h1>` with `... >PRISM</h1>`.
- [ ] 2.2 Update `<title>` tags in `web/layouts/_default/baseof.html` to use PRISM.

## 3. Hugo UI: Individual Pages (`web/layouts/audits/single.html`)
- [ ] 3.1 Create the directory `web/layouts/audits/`.
- [ ] 3.2 Move the content of `web/layouts/_default/single.html` into `web/layouts/audits/single.html`.
- [ ] 3.3 Remove the `{{ range .Site.Data.organisations }}` outer loop.
- [ ] 3.4 Fetch the specific organization data using the frontmatter ID: 
  `{{ $id := .Params.data_id }}`
  `{{ $orgArray := index .Site.Data.organisations $id }}`
  `{{ $org := index $orgArray 0 }}`
- [ ] 3.5 Ensure all partials (`itn-scorecard.html`, `impact-pathway.html`, etc.) are passed `$org`.
- [ ] 3.6 Add a simple `<a href="/audits/">&larr; Back to Directory</a>` near the top of the page.

## 4. Hugo UI: Master Table (`web/layouts/audits/list.html`)
- [ ] 4.1 Create `web/layouts/audits/list.html`.
- [ ] 4.2 Build an HTML `<table>` with Tailwind classes (`w-full text-left border-collapse`, etc.).
- [ ] 4.3 Range over all pages in the section `{{ range .Pages }}`.
- [ ] 4.4 For each page, fetch its data `{{ $orgArray := index .Site.Data.organisations .Params.data_id }} {{ $org := index $orgArray 0 }}`.
- [ ] 4.5 Extract and render the table columns:
  - **Charity Name:** `<a href="{{ .RelPermalink }}">{{ $org.name }}</a>`
  - **Neglectedness:** Calculate primary beneficiary type.
  - **Importance:** Calculate sum of beneficiaries.
  - **Tractability:** Extract highest evidence quality.
  - **Value for Money:** Extract `cost_per_outcome` from `$org.analytics.calculated_metrics`.
- [ ] 4.6 Include a lightweight, Vanilla JS sorting script at the bottom of the layout to allow users to click table headers (e.g., `<th>Cost per Outcome</th>`) to sort the rows ascending/descending.