# Change: Add Text Fragment Highlights to Source URLs

## Why
Currently, PRISM surfaces verifiable `source_url` links for impact metrics and significant events. However, clicking these links takes the user to the top of the referenced web page or PDF, requiring them to manually hunt for the specific claim. To enhance user experience, trust, and immediate verifiability, the UI should leverage W3C Text Fragments (`#:~:text=`) to open the link in a new tab and automatically scroll to and highlight the exact original quote.

## What Changes
- **Schema Update:** Add an optional `source_quote` field to the `significant_events` array in `impact.schema.json` to store the exact verbatim text (similar to the existing `evidence_quote` in the `metrics` array).
- **Prompt Engineering:** Update the `impact.system.md` LLM prompt to instruct the model to extract the exact, verbatim sentence into `source_quote` whenever an event is pulled from the source context.
- **UI/Hugo Refactoring:** - Update `web/layouts/partials/impact-pathway.html` to pass the newly available `source_quote` (for events) and `evidence_quote` (for metrics) into the `impact-item.html` partial.
  - Update `web/layouts/partials/impact-item.html` to dynamically construct the text fragment URL by appending `#:~:text=[URL_ENCODED_QUOTE]` to the `href` attribute if a quote is provided.

## Impact
- **Affected specs:** `data-schemas`, `audit-workflows`, `ui`
- **Affected code:** `schemas/v1/impact.schema.json`, `n8n/prompt-templates/impact.system.md`, `web/layouts/partials/impact-pathway.html`, `web/layouts/partials/impact-item.html`