## MODIFIED Requirements

### Requirement: Impact Evidence Standards
The schema SHALL structure impact data according to the "Hierarchy of Evidence" based on self-reported data, and MUST enforce brevity to ensure downstream presentation layers remain scannable.

#### Scenario: Grading Evidence Quality
- **WHEN** extracting impact data
- **THEN** the `evidence_quality` field MUST be an Enum restricted to:
  - `"RCT/Meta-Analysis"` (Gold standard)
  - `"Quasi-Experimental"` (Control groups used)
  - `"Pre-Post"` (Before/After comparison only)
  - `"Anecdotal"` (Stories/Testimonials only)
  - `"None"` (No data provided)
- **AND** narrative fields such as `context_qualifier` and `counterfactual_baseline.description` MUST be synthesized into concise, UI-friendly strings.