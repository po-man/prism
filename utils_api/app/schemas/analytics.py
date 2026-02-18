from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from app.services.model_generator import create_dynamic_model


AuditResult = create_dynamic_model("v1/analytics.schema.json")
AuditCheckItem = AuditResult.model_fields["check_items"].annotation.__args__[0]
AuditDetails = AuditCheckItem.model_fields["details"].annotation