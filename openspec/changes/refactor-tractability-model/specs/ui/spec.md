## MODIFIED Requirements

### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes.

#### Scenario: Displaying Intervention-Based Tractability
- **WHEN** rendering the "Tractability" card on the ITN Scorecard
- **THEN** the UI MUST derive the tractability score and description from the `analytics.check_items` array (specifically `check_intervention_tractability`), rather than parsing the `evidence_quality` from the raw impact metrics.
- **AND** it MUST display the highest matched EA evidence tier (e.g., "Quasi-Experimental") as the primary metric.
- **AND** it MUST display the EA rationale string (from the audit details) as the supporting text, replacing the charity's self-reported quote.