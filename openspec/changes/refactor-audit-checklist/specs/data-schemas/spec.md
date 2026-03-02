# openspec/changes/refactor-audit-checklist/specs/data-schemas/spec.md

## MODIFIED Requirements

### Requirement: EA Analytics Schema Expansion
The system SHALL define check items specific to Effective Altruism principles, strictly separating compliance-style checks from informational calculations.

#### Scenario: Enforcing Strict Boolean Audits and Decoupling Calculations
- **WHEN** the `analytics.schema.json` is validated
- **THEN** the `check_items.items.properties.status` enum MUST ONLY allow `["pass", "fail", "warning"]`. The `"null"` value MUST be removed.
- **AND** the root of the schema MUST include a new array property named `calculated_metrics` alongside `check_items`.
- **AND** items within `calculated_metrics` MUST include `id` (string), `name` (string), `value` (number or string), and `details` (object containing `formula` and `calculation`).