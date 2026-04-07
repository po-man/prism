from pydantic import BaseModel
from typing import Optional

from app.schemas.impact_beneficiaries import ImpactBeneficiaries
from app.schemas.impact_interventions import ImpactInterventions
from app.schemas.impact_metrics import ImpactMetrics
from app.schemas.impact_transparency import ImpactTranspar

class Impact(BaseModel):
    beneficiaries: Optional[ImpactBeneficiaries] = None
    interventions: Optional[ImpactInterventions] = None
    metrics: Optional[ImpactMetrics] = None
    transparency: Optional[ImpactTranspar] = None