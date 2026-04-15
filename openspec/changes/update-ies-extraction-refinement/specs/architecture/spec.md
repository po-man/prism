## MODIFIED Requirements

### Requirement: Separation of Concerns
The architecture SHALL strictly decouple orchestration, intelligence extraction, data validation, and frontend rendering.

#### Scenario: Generic Species Fallback Decoupling
- **WHEN** the `utils_api` calculates the Impact Equivalency Score (IES) and encounters an unmapped species
- **THEN** it MUST NOT rely on hardcoded Python dictionaries to resolve the fallback.
- **AND** it MUST query the `ref_moral_weights` reference collection in PocketBase for generic baseline records (e.g., `generic_companion`, `generic_farmed`, `generic_wild`, `generic_unspecified`) based on the charity's dominant beneficiary domain.

### Requirement: EA Animal Advocacy Audit Logic
The `utils_api` microservice SHALL execute deterministic audit functions, utilizing a standardized Pass/Warn/Fail three-tier thresholding system, separating intervention-level tractability from organisation-level monitoring capabilities.

#### Scenario: IES Calculation Bounding & Filtering
- **WHEN** the impact engine processes the `impact.metrics.metrics` array for IES calculation
- **THEN** it MUST apply a pre-processing filter to exclude any metric where `timeframe != 'annual'`.
- **AND** it MUST calculate the sum of `outcome.value` for all processed annual metrics.
- **AND** if this sum exceeds the sum of all unique individuals defined in `impact.beneficiaries.beneficiaries`, the engine MUST apply a bounding cap (ratio) to the total outcome pool to prevent mathematical inflation via duplicated metrics.

#### Scenario: Metric-to-Intervention Attribution
- **WHEN** the impact engine attempts to map a metric to a significant event to determine the Leverage Multiplier ($W_{leverage}$)
- **THEN** it MUST utilise a fuzzy matching heuristic (e.g., substring normalisation or Levenshtein distance) rather than strict exact-string matching.
- **AND** if an explicit match still fails, the engine MUST NOT drop the metric; instead, it MUST assign the metric to the charity's primary intervention or apply a conservative sector-average baseline probability.

#### Scenario: Leverage Multiplier ($W_{leverage}$) Resolution
- **WHEN** an event is tagged with multiple interventions
- **THEN** the engine MUST identify the intervention marked as `is_primary` and exclusively apply its $W_{leverage}$.
- **AND** it MUST NOT default to selecting the maximum $W_{leverage}$ from the array.