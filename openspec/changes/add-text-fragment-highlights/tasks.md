## 1. Schema Updates (`schemas`)
- [ ] 1.1 In `schemas/v1/impact.schema.json`, locate the `significant_events.items.properties` object.
- [ ] 1.2 Add an optional `"source_quote"` property (type: `["string", "null"]`, description: "The exact wording quoted from the official source validating the event summary.").

## 2. Prompt Engineering (`n8n/prompt-templates`)
- [ ] 2.1 In `n8n/prompt-templates/impact.system.md`, update the "Verbatim Evidence" instruction (currently rule #7) to read: "You must extract the exact, verbatim sentence from the text that justifies the claim. Place this exact sentence in the `evidence_quote` field for metrics, and the `source_quote` field for significant events."

## 3. Python Audit Engine (`utils_api`)
- [ ] 3.1 Restart the `utils_api` FastAPI server (or rebuild the Docker container) to flush the `lru_cache` and allow `create_dynamic_model` to pick up the new `source_quote` schema definition.

## 4. UI/UX Refactoring (`web`)
- [ ] 4.1 In `web/layouts/partials/impact-pathway.html`, update the `range $firstThreeEvents` and `range $restEvents` loops. Modify the `dict` passed to the partial to include the new quote field: 
  `{{ partial "impact-item.html" (dict "icon" "activity" "text" (.summary | default .event_name) "url" .source_url "quote" .source_quote) }}`.
- [ ] 4.2 In `web/layouts/partials/impact-pathway.html`, update the `range $firstThreeMetrics` and `range $restMetrics` loops to explicitly pass the metric's evidence quote:
  `{{ partial "impact-item.html" (dict "icon" "outcome" "text" $metricText "url" .source_url "quote" .evidence_quote) }}`.
- [ ] 4.3 In `web/layouts/partials/impact-item.html`, update the link rendering logic to append the text fragment if `.quote` exists. Example implementation for the `<a>` tag `href` attribute:
  `href="{{ .url }}{{ with .quote }}#:~:text={{ . | urlquery | replace "+" "%20" }}{{ end }}"`