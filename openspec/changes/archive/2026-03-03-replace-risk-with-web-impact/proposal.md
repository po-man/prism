# Change: Replace Risk Assessment with Web-Sourced Impact Extraction

## Why
The current system allocates significant architectural and cognitive overhead to a "Risk" assessment feature, which distracts from our core value proposition of Effective Altruism (EA) Impact Alignment. Furthermore, because grassroots animal advocacy charities often lack formal PDF annual reports, the system currently misses critical impact metrics. By deprecating Risk and redirecting that computational budget toward web-scraping and unstructured data extraction from official charity websites, we can evaluate a much broader and highly neglected segment of the sector.

## What Changes
- **BREAKING**: Deprecate the entire "Risk" feature. This includes removing the `risk` property from the core `OrganisationRecord` data model, deleting the associated JSON schema, and stripping the risk extraction branch from the n8n orchestration pipeline.
- Add a new web search and aggregation module to the n8n pipeline that explicitly queries the charity's official domain (derived from the metadata extraction) for impact-related snippets and articles.
- Update the `impact.schema.json` to include an optional `source_url` field for all metrics and significant events to maintain strict data provenance for web-sourced claims.
- Modify the Gemini impact extraction prompts to accept a fusion of PDF text (if available) and `<web_context>` snippets, with explicit instructions on evidence hierarchy.
- Refactor the Hugo UI to remove all Risk badges and leverage the new `source_url` field to create direct, verifiable hyperlinks from the rendered Impact Pathway directly to the charity's web claims.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** - `schemas/v1/impact.schema.json`
  - `schemas/v1/risk.schema.json` (to be deleted)
  - `utils_api/app/schemas/organisation.py`
  - `n8n/prompt-templates/impact.system.md`
  - `n8n/prompt-templates/impact.user.md`
  - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`
  - `web/layouts/_default/single.html`
  - `web/layouts/partials/impact-pathway.html`
  - `web/layouts/partials/impact-item.html`