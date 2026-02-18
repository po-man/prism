from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import AuditCheckItem, AuditDetails


def check_remuneration(record: OrganisationRecord) -> AuditCheckItem:
    """Checks for the presence of a remuneration package review report."""
    base_details = AuditDetails(
        formula="Presence of rem_pkg_review_report",
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_remuneration", status="null", significance="LOW", category="Governance", details=base_details
    )

    if not record.governance or not record.governance.remuneration_disclosure or record.governance.remuneration_disclosure.source_document_present is None:
        base_item.details.calculation = "Governance data for remuneration report is missing."
        return base_item

    if record.governance.remuneration_disclosure.source_document_present:
        base_item.status = "pass"
        base_item.details.calculation = "Remuneration package review report is present."
    else:
        base_item.status = "fail"
        base_item.details.calculation = "Remuneration package review report is not present."

    return base_item