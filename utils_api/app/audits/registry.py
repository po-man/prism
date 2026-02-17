from app.audits import financial
from app.audits import governance

# The registry holds all audit functions to be executed.
# This pattern makes it easy to add new checks without modifying the endpoint logic.
AUDIT_CHECKS = [
    # Financial Checks
    financial.check_reserve_cap,
    financial.check_liquidity,
    # Governance Checks
    governance.check_remuneration,
]