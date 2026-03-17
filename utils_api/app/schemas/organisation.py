from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.meta import Metadata
from app.schemas.impact import Impact, Metric
from app.schemas.financials import Financials


class OrganisationRecord(BaseModel):
    """
    Represents the data record for a single organisation, serving as input for the audit.
    """
    meta: Optional[Metadata] = None
    financials: Optional[Financials] = None
    impact: Optional[Impact] = None