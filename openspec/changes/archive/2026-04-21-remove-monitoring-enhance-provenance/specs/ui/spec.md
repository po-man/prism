## MODIFIED Requirements

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, providing direct, highlighted verification links for web-sourced claims and counterfactual baselines.

#### Scenario: Rendering Counterfactual Provenance
- **WHEN** rendering the "What would happen without this charity?" section in the Impact Pathway
- **THEN** the UI MUST display the verbatim `source.quote` instead of a synthesised description.
- **AND** the UI MUST render a provenance badge next to the quote.
- **AND** if a `source.url` is present, the badge MUST be hyperlinked using W3C Text Fragment syntax (`#:~:text=`) to highlight the quote on the target page.

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user on a dedicated organisation page.

#### Scenario: Exposing Audit Evaluation Rules
- **WHEN** a user clicks to expand a `<details>` element in the Audit Checklist
- **THEN** the expanded area MUST cleanly separate into a top "Evaluation Criteria" block and a bottom "Result" block.
- **AND** the top block MUST render the `details.criteria` string provided by the audit engine, styled with a muted background (e.g., `bg-gray-50`) to indicate it is a static rule.
- **AND** the bottom block MUST render the charity-specific `details.calculation` and `details.elaboration` (rendered as an italicised blockquote) to show how they performed against the rule.
- **AND** all hardcoded threshold tooltips (`$tooltips` dictionary) MUST be removed from the Hugo template.