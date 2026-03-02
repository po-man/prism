from pydantic import BaseModel, Field
from typing import Optional

from app.services.model_generator import create_dynamic_model


# Dynamically create Pydantic models from JSON schemas
OrganisationMetadata = create_dynamic_model("v1/meta.schema.json")
OrganisationFinancials = create_dynamic_model("v1/financials.schema.json")
OrganisationImpact = create_dynamic_model("v1/impact.schema.json")
OrganisationRisk = create_dynamic_model("v1/risk.schema.json")
Metric = OrganisationImpact.model_fields["metrics"].annotation.__args__[0]

class OrganisationRecord(BaseModel):
    """
    Represents the data record for a single organisation, serving as input for the audit.
    """
    meta: Optional[OrganisationMetadata] = None
    financials: Optional[OrganisationFinancials] = None
    impact: Optional[OrganisationImpact] = None
    risk: Optional[OrganisationRisk] = None