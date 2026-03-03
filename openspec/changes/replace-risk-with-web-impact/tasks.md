# openspec/changes/replace-risk-with-web-impact/tasks.md

## 1. Schema Refactoring (`schemas` & `utils_api`)
- [x] 1.1 Delete `schemas/v1/risk.schema.json`.
- [x] 1.2 In `schemas/v1/impact.schema.json`, add an optional `source_url` (type: `["string", "null"]`) to the `metrics.items.properties` object.
- [x] 1.3 In `schemas/v1/impact.schema.json`, add an optional `source_url` (type: `["string", "null"]`) to the `significant_events.items.properties` object.
- [x] 1.4 In `utils_api/app/schemas/organisation.py`, remove the `risk: Optional[OrganisationRisk] = None` field from the `OrganisationRecord` model, and remove the `OrganisationRisk` dynamic model initialization.
- [x] 1.5 In `utils_api/app/routers/audit.py`, remove `risk` from the `run_audit` endpoint payload/processing if explicitly referenced.

## 2. Prompt Engineering (`n8n/prompt-templates`)
- [ ] 2.1 Delete `risk.system.md` and `risk.user.md`.
- [ ] 2.2 In `impact.system.md`, add instructions: "You will be provided with official PDF text (if available) and `<web_context>` snippets from the charity's official website. Prioritize PDF data over web snippets if discrepancies exist. If you extract a metric or event from the `<web_context>`, you MUST populate its `source_url` property with the URL found in the snippet."
- [ ] 2.3 In `impact.user.md`, append the placeholder `<web_context>\n{{WEB_SEARCH_SNIPPETS}}\n</web_context>` to the bottom of the prompt.

## 3. n8n Orchestration Workflow (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 3.1 Open the workflow and delete the entire "Risk" branch: `Call 'Prompt Injection' - Risk`, `Extract Risk`, `Parsed Content (Risk)`, `Schema Validation (Risk)`, and `Storage API - Update Charity - Risk`.
- [ ] 3.2 Update the `Wait until all analysis done` Merge node to accept 2 inputs (Financials, Impact) instead of 3.
- [ ] 3.3 Add an HTTP Request node (e.g., Google Custom Search API) after `Parsed Content (Metadata)` to query `site:{{ $json.parsedContentObject.domains[0] }} (impact OR rescued OR animals OR annual OR report OR metrics)`.
- [ ] 3.4 Add a Code node to aggregate the search results into a single string formatted as `URL: [link]\nSnippet: [snippet]\n\n` and assign it to a variable (e.g., `web_snippets`).
- [ ] 3.5 Update the routing logic leading to the Impact branch: allow execution if `annual_report` exists OR if `web_snippets` is not empty.
- [ ] 3.6 Update the `Call 'Prompt Injection' - Impact` node to pass `WEB_SEARCH_SNIPPETS: $json.web_snippets` in its `injection_dict`.

## 4. PocketBase Database Migration (`pocketbase/migrations/`)
- [ ] 4.1 Create a new migration file to remove the `risk` JSON field from the `organisations` collection to align the database schema with the application logic.

## 5. UI / Hugo Refactoring (`web`)
- [ ] 5.1 In `web/layouts/_default/single.html`, delete the Go template block rendering the `$org.risk.data.overall_risk_level` badge.
- [ ] 5.2 In `web/layouts/partials/impact-item.html`, update the template to accept a URL parameter. If a URL is provided, wrap the `text` span or specific segment in `<a href="{{ .url }}" target="_blank" class="hover:text-blue-600 hover:underline">...</a>`.
- [ ] 5.3 In `web/layouts/partials/impact-pathway.html`, update the rendering loops for `$impact.significant_events` and `$impact.metrics` to pass the newly available `.source_url` into the `impact-item.html` partial dictionary (e.g., `(dict "icon" "activity" "text" .summary "url" .source_url)`).