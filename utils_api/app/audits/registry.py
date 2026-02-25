from app.audits import financial, impact

# The registry holds all audit functions to be executed.
# This pattern makes it easy to add new checks without modifying the endpoint logic.
AUDIT_CHECKS = [
    # Financial Checks
    financial.check_reserve_cap,
    financial.check_liquidity,
    # Impact Checks
    impact.check_evidence_quality,
    impact.check_counterfactual_baseline,
    impact.check_cost_per_outcome,
    impact.check_funding_neglectedness,
    impact.check_cause_area_neglectedness,
]