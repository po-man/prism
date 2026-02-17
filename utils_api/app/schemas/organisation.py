from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class OrganisationFinancials(BaseModel):
    """Schema for an organisation's financial data."""
    lsg_reserve_amount: Optional[float] = None
    operating_expenditure: Optional[float] = None
    net_current_assets: Optional[float] = None
    monthly_operating_expenses: Optional[float] = None

class OrganisationGovernance(BaseModel):
    """Schema for an organisation's governance data."""
    rem_pkg_review_report_present: Optional[bool] = Field(None, alias="rem_pkg_review_report")

class OrganisationRecord(BaseModel):
    """
    Represents the data record for a single organisation, serving as input for the audit.
    """
    financials: Optional[OrganisationFinancials] = None
    governance: Optional[OrganisationGovernance] = None
    # other top-level fields like 'impact', 'risk' can be added here