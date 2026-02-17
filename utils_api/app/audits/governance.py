from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import AuditCheckItem, AuditDetails

def check_remuneration(record: OrganisationRecord) -> AuditCheckItem:
    """Checks for the presence of a remuneration package review report."""
    # This is a skeleton. Full implementation will follow.
    return AuditCheckItem(
        id="check_remuneration",
        status="null",
        significance="LOW",
        category="Governance",
        details=AuditDetails(formula="Presence of rem_pkg_review_report", calculation="Not computed")
    )