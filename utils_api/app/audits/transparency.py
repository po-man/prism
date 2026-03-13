from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import AuditCheckItem, AuditDetails


def check_negative_impact_disclosure(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks if the organization reported on unintended negative impacts.
    This is an advanced check that rewards transparency.
    """
    details = AuditDetails(
        formula="Check for self-reported unintended consequences or failures.",
        calculation="Not computed",
        elaboration="This check rewards epistemic humility. Non-disclosure is standard and not a failure.",
    )
    item = AuditCheckItem(
        id="check_negative_impact_disclosure",
        status="not_disclosed",
        significance="MEDIUM",
        category="Transparency",
        details=details,
    )

    disclosure = False
    if (
        record.impact
        and record.impact.transparency_indicators
        and record.impact.transparency_indicators.unintended_consequences_reported
    ):
        disclosure = record.impact.transparency_indicators.unintended_consequences_reported.value

    if disclosure:
        item.status = "bonus"
        item.details.calculation = "Organisation self-reported on unintended negative impacts."
    else:
        item.status = "not_disclosed"
        item.details.calculation = "No disclosure of unintended negative impacts found. This is the industry norm."

    return item


def check_live_release_transparency(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks if organizations engaged in direct rescue provide euthanasia/live-release data.
    This is a conditional advanced check.
    """
    details = AuditDetails(
        formula="For direct rescue orgs, check for euthanasia/live-release rate disclosure.",
        calculation="Not computed",
        elaboration=None,
    )
    item = AuditCheckItem(
        id="check_live_release_transparency",
        status="not_disclosed",
        significance="HIGH",
        category="Transparency",
        details=details,
    )

    applicable_interventions = {"individual_rescue_and_sanctuary", "veterinary_care_and_treatment"}
    is_applicable = False
    if record.impact and record.impact.significant_events:
        is_applicable = any(
            intervention in applicable_interventions
            for event in record.impact.significant_events
            for intervention in event.intervention_type
        )

    if not is_applicable:
        item.status = "n_a"
        item.details.calculation = "Organisation does not engage in direct animal sheltering; metric not applicable."
        return item

    disclosure = False
    if (
        record.impact
        and record.impact.transparency_indicators
        and record.impact.transparency_indicators.euthanasia_statistics_reported
    ):
        disclosure = record.impact.transparency_indicators.euthanasia_statistics_reported.value

    if disclosure:
        item.status = "bonus"
        item.details.calculation = "Organisation provided euthanasia or live-release statistics."
    else:
        item.status = "not_disclosed"
        item.details.calculation = "No disclosure of euthanasia or live-release rates found."

    item.details.elaboration = "This check rewards transparency for a sensitive operational metric."
    return item