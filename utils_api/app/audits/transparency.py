from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import CheckItem, Details


def check_negative_impact_disclosure(record: OrganisationRecord) -> CheckItem:
    """
    Checks if the organization reported on unintended negative impacts.
    This is an advanced check that rewards transparency.
    """
    details = Details(
        formula="Check for self-reported unintended consequences or failures.",
        calculation="Not computed",
        criteria="Bonus: Organisation self-reported on unintended negative impacts. | Not Disclosed: No disclosure found.",
        elaboration="This check rewards epistemic humility. Non-disclosure is standard and not a failure.",
    )
    item = CheckItem(
        id="check_negative_impact_disclosure",
        status="not_disclosed",
        significance="MEDIUM",
        category="Transparency",
        details=details,
    )

    disclosure_indicator = None
    if (
        record.impact
        and record.impact.transparency
        and record.impact.transparency.transparency_indicators
        and record.impact.transparency.transparency_indicators.unintended_consequences_reported
    ):
        disclosure_indicator = record.impact.transparency.transparency_indicators.unintended_consequences_reported

    if disclosure_indicator and disclosure_indicator.value:
        item.status = "bonus"
        item.details.calculation = "Organisation self-reported on unintended negative impacts."
        if disclosure_indicator.source and disclosure_indicator.source.quote:
            item.details.elaboration = f"Quote: '{disclosure_indicator.source.quote}'"
        else:
            item.details.elaboration = "Disclosure confirmed, but quote was not provided."
    else:
        item.status = "not_disclosed"
        item.details.calculation = "No disclosure of unintended negative impacts found. This is the industry norm."

    return item


def check_live_release_transparency(record: OrganisationRecord) -> CheckItem:
    """
    Checks if organizations engaged in direct rescue provide euthanasia/live-release data.
    This is a conditional advanced check.
    """
    details = Details(
        formula="For direct rescue orgs, check for euthanasia/live-release rate disclosure.",
        calculation="Not computed",
        criteria="Bonus: Euthanasia/live-release data is disclosed. | Not Disclosed: No disclosure found. | N/A: Not applicable for non-sheltering organisations.",
        elaboration=None,
    )
    item = CheckItem(
        id="check_live_release_transparency",
        status="not_disclosed",
        significance="HIGH",
        category="Transparency",
        details=details,
    )

    applicable_interventions = {"individual_rescue_and_sanctuary", "veterinary_care_and_treatment"}
    is_applicable = False
    if record.impact and record.impact.interventions and record.impact.interventions.significant_events:
        is_applicable = any(
            intervention.value in applicable_interventions
            for event in record.impact.interventions.significant_events
            for intervention in event.intervention_type
        )

    if not is_applicable:
        item.status = "n_a"
        item.details.calculation = "Organisation does not engage in direct animal sheltering; metric not applicable."
        return item

    disclosure_indicator = None
    if (
        record.impact
        and record.impact.transparency
        and record.impact.transparency.transparency_indicators
        and record.impact.transparency.transparency_indicators.euthanasia_statistics_reported
    ):
        disclosure_indicator = record.impact.transparency.transparency_indicators.euthanasia_statistics_reported

    if disclosure_indicator and disclosure_indicator.value:
        item.status = "bonus"
        item.details.calculation = "Organisation provided euthanasia or live-release statistics."
        if disclosure_indicator.source and disclosure_indicator.source.quote:
            item.details.elaboration = f"Quote: '{disclosure_indicator.source.quote}'"
        else:
            item.details.elaboration = "Disclosure confirmed, but quote was not provided."
    else:
        item.status = "not_disclosed"
        item.details.calculation = "No disclosure of euthanasia or live-release rates found."
        item.details.elaboration = "This check rewards transparency for a sensitive operational metric."
    return item