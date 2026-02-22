from pydantic import BaseModel, Field
from typing import Optional

from app.services.model_generator import create_dynamic_model


# Dynamically create Pydantic models from JSON schemas
OrganisationFinancials = create_dynamic_model("v1/financials.schema.json")
OrganisationGovernance = create_dynamic_model("v1/governance.schema.json")
OrganisationImpact = create_dynamic_model("v1/impact.schema.json")

class OrganisationRecord(BaseModel):
    """
    Represents the data record for a single organisation, serving as input for the audit.
    """
    financials: Optional[OrganisationFinancials] = None
    governance: Optional[OrganisationGovernance] = None
    impact: Optional[OrganisationImpact] = None
    # other top-level fields like 'risk' can be added here