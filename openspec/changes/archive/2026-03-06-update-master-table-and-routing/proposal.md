## Why
Currently, PRISM's master table is hosted at `/audits/` and organizations at `/audits/<slug>`, creating unnecessary nesting. Moving the master table to the root (`/`) and organizations to `/<slug>` creates a cleaner, more shareable URL structure. Furthermore, the master table currently relies on text labels for "Neglectedness" and lacks visibility into Data Provenance. By elevating the Data Source icons and proportional Beneficiary Type icons to the master table, we allow donors to perform rapid, at-a-glance comparisons of charity transparency and cause-area focus before navigating to individual report cards.

## What Changes
1. **URL & Routing Flattening:** - Update the n8n pipeline to write markdown stubs directly to `web/content/` instead of `web/content/audits/`, and remove the `type: "audits"` frontmatter.
   - Refactor Hugo layouts: migrate the master list template to `layouts/index.html` (the site root) and the organization detail template to `layouts/_default/single.html`.
2. **Master Table UI - Data Sources:** Add a "Data Sources" column to the master table, reusing the icon logic from the organization profile (Annual Report, Financials, Web Search) with grayscale/opacity indicators for missing data.
3. **Master Table UI - Beneficiaries:** Replace the text-based "Target Species (Neglectedness)" column with visual SVG badges representing the beneficiary types (Companion, Farmed, Wild). The opacity of each badge will dynamically reflect the calculated proportion of that beneficiary type relative to the charity's total beneficiaries.

## Impact
- **Affected specs:** `ui`
- **Affected code:** - `n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json` (Markdown Stub & Write to File nodes)
  - `web/layouts/audits/list.html` (Moved to `web/layouts/index.html`)
  - `web/layouts/audits/single.html` (Moved to `web/layouts/_default/single.html`)