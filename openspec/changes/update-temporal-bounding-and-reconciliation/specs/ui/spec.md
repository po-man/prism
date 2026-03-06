## MODIFIED Requirements

### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence, while explicitly bounding and labelling temporal scopes.

#### Scenario: Explicit Temporal Labelling on Scorecards
- **WHEN** rendering the Importance and Neglectedness sections of the scorecard
- **THEN** the UI MUST display a small, unobtrusive tag (e.g., "Annual") in the top-right corner of the respective cards.
- **AND** this tag MUST clearly indicate to the user that these specific metrics represent a single-year snapshot, preventing confusion with cumulative historical data.