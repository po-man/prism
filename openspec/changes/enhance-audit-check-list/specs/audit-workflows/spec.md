## ADDED Requirements

### Requirement: Impact Awareness Computation
The system MUST compute a series of check-items based on extracted Effective Altruism impact data to evaluate an organization's impact rigor and funding landscape.

#### Scenario: Evaluating Evidence Quality
- **GIVEN** an NGO's extracted impact data contains only "Anecdotal" or "Low" evidence quality
- **WHEN** the audit logic evaluates impact awareness
- **THEN** the `check_evidence_quality` item MUST return `status: "warning"`
- **AND** include a recommendation in the details field to adopt rigorous evaluation frameworks.

#### Scenario: Cost per Outcome Estimation
- **GIVEN** an NGO has `program_services` expenditure of $1,000,000 and a primary intervention reaching 5,000 beneficiaries
- **WHEN** the audit logic calculates cost-effectiveness
- **THEN** the `check_cost_per_outcome` item MUST record the calculated cost ($200 per beneficiary) in the `details.calculation` field
- **AND** MUST NOT assign a `pass` or `fail` status, as this metric is strictly informational for cross-charity comparison.

#### Scenario: Funding Neglectedness Flagging
- **GIVEN** an NGO receives 95% of its total income from government subventions
- **WHEN** the audit logic evaluates funding neglectedness
- **THEN** the `check_funding_neglectedness` item MUST return `status: "warning"`
- **AND** explicitly note in the details that marginal private donations may have lower counterfactual impact due to high government support.