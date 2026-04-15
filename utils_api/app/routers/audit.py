from fastapi import APIRouter, Body
from typing import List
import asyncio

from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import Analytics, CheckItem, CalculatedMetric
from app.audits.registry import AUDIT_CHECKS, METRIC_CALCULATORS, ASYNC_METRIC_CALCULATORS

router = APIRouter()

@router.post("/audit", response_model=Analytics, tags=["Auditing"])
async def run_audit(record: OrganisationRecord = Body(...)):
    """
    Runs a series of audit checks against an organisation's data record.

    - **Input**: An object matching the OrganisationRecord schema.
    - **Output**: An object matching the analytics.schema.json, containing the results of all checks.
    """
    # Run synchronous audit checks
    check_items: List[CheckItem] = [check(record) for check in AUDIT_CHECKS]
    
    # Run synchronous metric calculators
    calculated_metrics: List[CalculatedMetric] = []
    for calculator in METRIC_CALCULATORS:
        if (metric := calculator(record)) is not None:
            calculated_metrics.append(metric)

    # Run asynchronous metric calculators concurrently
    async_tasks = [calculator(record) for calculator in ASYNC_METRIC_CALCULATORS]
    async_results = await asyncio.gather(*async_tasks)
    for metric in async_results:
        if metric is not None:
            calculated_metrics.append(metric)

    return Analytics(check_items=check_items, calculated_metrics=calculated_metrics)