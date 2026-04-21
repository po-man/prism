from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import CheckItem, Details
from app.audits.utils import resolve_value


def check_reserve_cap(record: OrganisationRecord) -> CheckItem:
    """
    Checks if general reserve is within a reasonable range of operating expenditure.
    - Pass: <= 2 years
    - Warn: > 2 and <= 5 years
    - Fail: > 5 years
    """
    base_details = Details(
        formula="total_reserves / total_expenditure",
        elaboration=None,
        criteria="Pass: <= 2 years of expenditure. | Warn: 2-5 years. | Fail: > 5 years.",
        calculation="Not computed",
    )
    base_item = CheckItem(id="check_reserve_cap", status="fail", significance="MEDIUM", category="Financial Health", details=base_details)

    if (
        not record.financials
        or not record.financials.reserves
        or not record.financials.reserves.total_reserves
        or record.financials.reserves.total_reserves.value is None
        or not record.financials.expenditure
        or not record.financials.expenditure.total
        or record.financials.expenditure.total.value is None
    ):
        base_item.details.calculation = "Required financial data is missing."
        return base_item

    reserve = resolve_value(record.financials.reserves.total_reserves)
    expenditure = resolve_value(record.financials.expenditure.total)

    if expenditure <= 0:
        base_item.status = "warning"
        base_item.details.calculation = f"Total expenditure (${expenditure:,.0f}) is not a positive number, cannot compute ratio."
        return base_item

    ratio_in_years = reserve / expenditure

    base_item.details.calculation = f"(${reserve:,.0f} / ${expenditure:,.0f}) = {ratio_in_years:.1f} years of expenditure"

    if ratio_in_years > 5:
        base_item.status = "fail"
    elif ratio_in_years > 2:
        base_item.status = "warning"
    else:
        base_item.status = "pass"

    return base_item


def check_liquidity(record: OrganisationRecord) -> CheckItem:
    """
    Checks if the liquidity ratio is sufficient.
    - Pass: >= 6 months
    - Warn: >= 3 and < 6 months
    - Fail: < 3 months
    """
    base_details = Details(
        formula="(current_assets - current_liabilities) / monthly_operating_expenses",
        elaboration=None,
        criteria="Pass: >= 6 months of operating expenses. | Warn: 3-6 months. | Fail: < 3 months.",
        calculation="Not computed",
    )
    base_item = CheckItem(id="check_liquidity", status="fail", significance="MEDIUM", category="Financial Health", details=base_details)

    if not record.financials or not record.financials.ratio_inputs:
        base_item.details.calculation = "Required financial data for liquidity check is missing."
        return base_item

    ratio_inputs = record.financials.ratio_inputs
    net_assets = resolve_value(ratio_inputs.net_current_assets) if ratio_inputs.net_current_assets else None
    monthly_expenses = resolve_value(ratio_inputs.monthly_operating_expenses) if ratio_inputs.monthly_operating_expenses else None
    calculation_string = ""

    if (
        net_assets is None
        and ratio_inputs.current_assets
        and ratio_inputs.current_assets.value is not None
        and ratio_inputs.current_liabilities
        and ratio_inputs.current_liabilities.value is not None
    ):
        current_assets = resolve_value(ratio_inputs.current_assets)
        current_liabilities = resolve_value(ratio_inputs.current_liabilities)
        net_assets = current_assets - current_liabilities
        if monthly_expenses is not None:
            calculation_string = f"((${current_assets:,.0f} - ${current_liabilities:,.0f}) / ${monthly_expenses:,.0f})"

    if net_assets is None or monthly_expenses is None:
        base_item.details.calculation = "Required financial data is missing."
        return base_item

    if monthly_expenses <= 0:
        # Assuming monthly_expenses can be 0, but not negative.
        base_item.status = "warning"
        base_item.details.calculation = f"Monthly operating expenses (${monthly_expenses:,.0f}) is not a positive number, cannot compute ratio."
        return base_item

    ratio = net_assets / monthly_expenses

    truncated_ratio = int(ratio * 10) / 10.0
    if not calculation_string:
        calculation_string = f"(${net_assets:,.0f} / ${monthly_expenses:,.0f})"

    base_item.details.calculation = f"{calculation_string} = {truncated_ratio:.1f} months"

    if ratio >= 6:
        base_item.status = "pass"
    elif ratio >= 3:
        base_item.status = "warning"
    else:
        base_item.status = "fail"

    return base_item