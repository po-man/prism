## ADDED Requirements

### Requirement: Interactive Provenance Badges
The UI SHALL render explicit, interactive citation badges for all quantitative figures and claims to facilitate immediate human verification against source documents.

#### Scenario: Rendering Document vs. Web Citations
- **WHEN** the Hugo template iterates over `beneficiaries`, `metrics`, `significant_events`, or `financials` that contain a populated `source` object
- **THEN** it MUST render a small UI badge adjacent to the claim (e.g., an icon with "📄 p. 12" for PDFs, or "🌐 Web" for web searches).
- **AND** the badge MUST be an anchor tag (`<a>`) linking to the `resolved_url`, ensuring the link opens in a new browser tab.
- **AND** the UI MUST expose the verbatim `quote` text either via a tooltip (e.g., standard `title` attribute) on the badge, or a collapsible `<details>` element beneath the claim, allowing the human reviewer to know exactly what text to scan for once the deep-link resolves.