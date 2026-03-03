## MODIFIED Requirements

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, prioritizing the most significant interventions to prevent cognitive overload, and providing direct, highlighted verification links for web-sourced claims.

#### Scenario: Expanding Top 3 Interventions
- **WHEN** rendering the "Activities & Outputs" and "Outcomes" columns
- **THEN** the UI MUST sort the items by significance (based on the array order provided by the LLM).
- **AND** it MUST display only the top 3 items by default.
- **AND** if more than 3 items exist, it MUST provide an interactive, offline-compatible toggle (e.g., "Show all X activities") to reveal the remaining items.

#### Scenario: Hyperlinking and Highlighting Web-Sourced Claims
- **WHEN** rendering the "Activities & Outputs" and "Outcomes" items in the Impact Pathway
- **THEN** the UI MUST check for the presence of the `source_url` field.
- **AND** if `source_url` is present, it MUST wrap the `metric_name` (or the `event_name`) in an HTML `<a>` tag with `target="_blank"` and `rel="noopener noreferrer"`.
- **AND** if an exact quote (`source_quote` or `evidence_quote`) is also present, the UI MUST URL-encode the quote and append it to the `href` using the W3C Text Fragment syntax (`#:~:text=`), ensuring the user's browser automatically scrolls to and highlights the claim.