from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import AuditCheckItem, AuditDetails

def check_reserve_cap(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks if LSG reserve is within the 25% cap of operating expenditure.
    Fail if > 0.25.
    """
    # This is a skeleton. Full implementation will follow.
    return AuditCheckItem(
        id="check_reserve_cap",
        status="null",
        significance="HIGH",
        category="Financial Health",
        details=AuditDetails(formula="lsg_reserve / operating_expenditure", calculation="Not computed")
    )

def check_liquidity(record: OrganisationRecord) -> AuditCheckItem:
    """Checks if the liquidity ratio is sufficient (>= 3 months)."""
    # This is a skeleton. Full implementation will follow.
    return AuditCheckItem(
        id="check_liquidity",
        status="null",
        significance="MEDIUM",
        category="Financial Health",
        details=AuditDetails(formula="net_current_assets / monthly_operating_expenses", calculation="Not computed")
    )