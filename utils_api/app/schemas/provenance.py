from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, AnyHttpUrl, Field

class ProvenanceContext(BaseModel):
    """
    Contextual information required to resolve provenance, including base URLs
    for attached reports.
    """

    attached_reports: List[AnyHttpUrl] = Field(default_factory=list)


class ProvenanceRequest(BaseModel):
    """
    The request payload for the /resolve-provenance endpoint, containing the
    data blob to be processed and the necessary context.
    """

    data: Union[Dict[str, Any], List[Dict[str, Any]]]
    context: ProvenanceContext