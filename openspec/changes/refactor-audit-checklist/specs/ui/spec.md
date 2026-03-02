# openspec/changes/refactor-audit-checklist/specs/ui/spec.md

## MODIFIED Requirements

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise and providing immediate threshold transparency to the user.

#### Scenario: Surfacing Threshold Logic via Tooltips
- **WHEN** rendering the `analytics.check_items` array in `audit-checklist.html`
- **THEN** the Hugo template MUST maintain an internal dictionary mapping `check_item.id` to a human-readable explanation of its thresholds (e.g., `"check_liquidity": "Pass: >=6 mos | Warn: 3-6 mos | Fail: <3 mos"`).
- **AND** this string MUST be injected into a `title` attribute or a custom tooltip UI element on the check item's header, allowing users to understand the evaluation criteria on hover.

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, pulling from dedicated calculation entities.

#### Scenario: Rendering Decoupled Calculations
- **WHEN** rendering the Value for Money component
- **THEN** the template MUST extract the Cost per Outcome data directly from the new `analytics.calculated_metrics` array, rather than parsing it out of the `check_items` array.