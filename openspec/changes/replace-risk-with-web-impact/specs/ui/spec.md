# openspec/changes/replace-risk-with-web-impact/specs/ui/spec.md

## MODIFIED Requirements

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, prioritizing the most significant interventions to prevent cognitive overload, and providing direct verification links for web-sourced claims.

#### Scenario: Hyperlinking Web-Sourced Claims
- **WHEN** rendering the "Activities & Outputs" and "Outcomes" items in the Impact Pathway
- **THEN** the UI MUST check for the presence of the `source_url` field.
- **AND** if `source_url` is present, it MUST wrap the `metric_name` (or the `event_name`) in an HTML `<a>` tag with `target="_blank"`, allowing the user to click directly through to the charity's website to verify the claim.

## REMOVED Requirements

### Requirement: Risk Badge Rendering
**Reason**: Risk is no longer calculated or stored by the system.
**Migration**: Remove the Risk level indicator badge (e.g., "Risk: LOW") from the charity header in the Hugo `single.html` template.