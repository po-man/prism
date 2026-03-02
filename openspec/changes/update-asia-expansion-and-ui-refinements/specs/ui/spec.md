# openspec/changes/update-asia-expansion-and-ui-refinements/specs/ui/spec.md

## MODIFIED Requirements

### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence.

#### Scenario: Displaying Cumulative Importance and Verifiable Tractability
- **WHEN** rendering the Importance section of the scorecard
- **THEN** the UI MUST compute and display the sum total of all populations across the `.impact.data.beneficiaries` array.
- **AND** it MUST explicitly display the demographic breakdown (e.g., specific species or beneficiary types) directly beneath the total "Affects up to X individuals" metric.
- **WHEN** rendering the Tractability section of the scorecard
- **THEN** the UI MUST display the highest `evidence_quality` achieved.
- **AND** it MUST display the exact `evidence_quote` associated with that metric to verify the claim, or provide an elaboration if a direct quote is unavailable.

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, using cumulative beneficiary mathematics.

#### Scenario: Displaying the Cumulative Cost per Outcome
- **WHEN** rendering the "Estimated Cost per Outcome" block in the Value for Money section
- **THEN** the calculation MUST utilize the sum of all primary beneficiaries, rather than the single highest maximum value.
- **AND** the UI MUST provide a hover-able tooltip over the calculation text that explains the exact formula used to derive the retail equivalent.

## ADDED Requirements

### Requirement: Impact Pathway Display
The UI SHALL present the charity's logic model hierarchically, prioritizing the most significant interventions to prevent cognitive overload.

#### Scenario: Expanding Top 3 Interventions
- **WHEN** rendering the "Activities & Outputs" and "Outcomes" columns
- **THEN** the UI MUST sort the items by significance (based on the array order provided by the LLM).
- **AND** it MUST display only the top 3 items by default.
- **AND** if more than 3 items exist, it MUST provide an interactive, offline-compatible toggle (e.g., "Show all X activities") to reveal the remaining items.

### Requirement: Audit Checklist Presentation
The UI SHALL render the deterministic audit results, filtering out noise to focus on actionable EA alignment data.

#### Scenario: Filtering Calculation-Only Items
- **WHEN** iterating through the `analytics.check_items` array
- **THEN** the UI MUST exclude any item where the `status` is exactly `"null"` (indicating a calculation-only informational item, such as Cost per Outcome).
- **AND** for items with a `pass`, `warning`, or `fail` status, the UI MUST render the `details.elaboration` text (if present) inside the expanded dropdown to provide qualitative context or exact quotes.