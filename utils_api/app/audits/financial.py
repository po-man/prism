from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import AuditCheckItem, AuditDetails


def check_reserve_cap(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks if LSG reserve is within the 25% cap of operating expenditure.
    Fail if > 0.25.
    """
    base_details = AuditDetails(
        formula="lsg_reserve_amount / total_expenditure",
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_reserve_cap", status="null", significance="HIGH", category="Financial Health", details=base_details
    )

    if (
        not record.financials
        or not record.financials.lsg_specifics
        or not record.financials.expenditure
        or record.financials.lsg_specifics.lsg_reserve_amount is None
        or record.financials.expenditure.total is None
    ):
        base_item.details.calculation = "Required financial data is missing."
        return base_item

    reserve = record.financials.lsg_specifics.lsg_reserve_amount
    expenditure = record.financials.expenditure.total

    if expenditure <= 0:
        base_item.status = "warning"
        base_item.details.calculation = f"Operating expenditure (${expenditure:,.0f}) is not a positive number, cannot compute ratio."
        return base_item

    ratio = reserve / expenditure
    cap = 0.25

    base_item.details.calculation = f"(${reserve:,.0f} / ${expenditure:,.0f}) = {ratio:.1%} (vs. {cap:.0%} cap)"

    if ratio > cap:
        base_item.status = "fail"
    else:
        base_item.status = "pass"

    return base_item


def check_liquidity(record: OrganisationRecord) -> AuditCheckItem:
    """Checks if the liquidity ratio is sufficient (>= 3 months). Fail if < 3."""
    base_details = AuditDetails(
        formula="net_current_assets / monthly_operating_expenses",
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_liquidity", status="null", significance="MEDIUM", category="Financial Health", details=base_details
    )

    if (
        not record.financials
        or not record.financials.ratio_inputs
        or record.financials.ratio_inputs.net_current_assets is None
        or record.financials.ratio_inputs.monthly_operating_expenses is None
    ):
        base_item.details.calculation = "Required financial data is missing."
        return base_item

    assets = record.financials.ratio_inputs.net_current_assets
    monthly_expenses = record.financials.ratio_inputs.monthly_operating_expenses

    if monthly_expenses <= 0:
        # Assuming monthly_expenses can be 0, but not negative.
        base_item.status = "warning"
        base_item.details.calculation = f"Monthly operating expenses (${monthly_expenses:,.0f}) is not a positive number, cannot compute ratio."
        return base_item

    ratio = assets / monthly_expenses
    threshold = 3

    truncated_ratio = int(ratio * 10) / 10.0
    base_item.details.calculation = f"(${assets:,.0f} / ${monthly_expenses:,.0f}) = {truncated_ratio:.1f} months"

    if ratio < threshold:
        base_item.status = "fail"
    else:
        base_item.status = "pass"

    return base_item