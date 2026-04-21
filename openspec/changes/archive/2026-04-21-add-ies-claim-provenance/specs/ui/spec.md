## MODIFIED Requirements

### Requirement: IES Transparent Breakdown Card
The UI SHALL render the calculated Impact Equivalency Score (IES) in a dedicated component on the individual charity profile, explicitly framing it as an exploratory, temporally bounded model rather than an absolute truth, and providing immediate verifiability for all claims.

#### Scenario: Rendering Provenance on Impact Claims
- **WHEN** iterating through the IES Calculation Breakdown table rows
- **THEN** the UI MUST render the `metric_name` string.
- **AND** if a `source` object is present at the breakdown item level, it MUST render the interactive provenance badge immediately succeeding the metric name.