from app.audits import financial, impact

# The registry holds all audit check functions to be executed.
# These functions are expected to return an `AuditCheckItem`.
AUDIT_CHECKS = [
    # Financial Checks
    financial.check_reserve_cap,
    financial.check_liquidity,
    # Impact Checks
    impact.check_evidence_quality,
    impact.check_counterfactual_baseline,
    impact.check_funding_neglectedness,
    impact.check_cause_area_neglectedness,
]

# This registry holds all metric calculation functions.
# These functions are expected to return a `CalculatedMetric` or `None`.
METRIC_CALCULATORS = [
    impact.calculate_cost_per_outcome,
]