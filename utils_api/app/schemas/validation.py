from pydantic import BaseModel
from typing import Dict, Any


class ValidationRequest(BaseModel):
    """Defines the request body for the /validate endpoint."""

    schema_name: str
    data: Dict[str, Any]