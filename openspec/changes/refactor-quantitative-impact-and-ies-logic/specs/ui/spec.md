## REMOVED Requirements

### Requirement: Impact Pathway Display
**Reason**: Qualitative activities and unstructured outcomes generate cognitive overload and detract from the strictly quantitative focus of Effective Altruism evaluations.
**Migration**: The counterfactual component will migrate to the Impact Profile, and the financial input component will migrate to the Value for Money section. The timeline of activities and general outcomes are deprecated.

## MODIFIED Requirements

### Requirement: ITN Scorecard Rendering
The static site generator (Hugo) SHALL render the Importance, Tractability, and Neglectedness scorecard for each charity, accurately reflecting cumulative impact and verbatim evidence, while immediately establishing the counterfactual baseline.

#### Scenario: Displaying the Counterfactual Context
- **WHEN** rendering the Impact Profile section
- **THEN** the UI MUST display the "What would happen without this charity?" block (if a valid counterfactual exists).
- **AND** it MUST be positioned prominently before the quantitative demographic breakdowns, rendering the exact source quote and its interactive provenance badge.

### Requirement: Overhead vs. Impact Myth-Buster Display
The UI SHALL present the estimated cost per outcome alongside a tangible retail donation equivalent, contextualizing administrative overhead with the absolute total financial inputs.

#### Scenario: Integrating Total Annual Expenditure
- **WHEN** rendering the Expense Breakdown column within the Value for Money section
- **THEN** the UI MUST dynamically calculate and render the Total Annual Expenditure in USD at the top of the card.
- **AND** it MUST include the original local currency and exchange rate as a hover-able tooltip on the total figure.