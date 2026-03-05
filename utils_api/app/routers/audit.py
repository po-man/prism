from fastapi import APIRouter, Body
from typing import List

from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import AuditResult, AuditCheckItem, CalculatedMetric
from app.audits.registry import AUDIT_CHECKS, METRIC_CALCULATORS

router = APIRouter()

@router.post("/audit", response_model=AuditResult, tags=["Auditing"])
async def run_audit(record: OrganisationRecord = Body(...)):
    """
    Runs a series of audit checks against an organisation's data record.

    - **Input**: An object matching the OrganisationRecord schema.
    - **Output**: An object matching the analytics.schema.json, containing the results of all checks.
    """
    check_items: List[AuditCheckItem] = [check(record) for check in AUDIT_CHECKS]
    
    calculated_metrics: List[CalculatedMetric] = []
    for calculator in METRIC_CALCULATORS:
        if (metric := calculator(record)) is not None:
            calculated_metrics.append(metric)

    return AuditResult(check_items=check_items, calculated_metrics=calculated_metrics)