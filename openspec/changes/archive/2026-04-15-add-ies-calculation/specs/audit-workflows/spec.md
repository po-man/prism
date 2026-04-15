## ADDED Requirements

### Requirement: Impact Equivalency Score (IES) Processing Flow
The orchestration pipeline SHALL execute a rigid, multi-stage data lineage to compute the IES using the formula $IES_i = Outcomes_i \times W_{species} \times W_{leverage} \times D_{evidence}$.

#### Scenario: Executing the IES Data Lineage
- **WHEN** the n8n orchestrator passes the extracted impact payload to the `utils_api`
- **THEN** the `utils_api` MUST query PocketBase for the corresponding $W_{species}$ and $D_{evidence}$ multipliers.
- **AND** the `utils_api` MUST query PocketBase for the programmatic BOTEC probability multiplier ($W_{leverage}$).
- **AND** the `utils_api` MUST compute the final IES integer using the explicitly extracted $Outcomes_i$ claims and append the detailed mathematical breakdown to the `calculated_metrics` array before persistence.