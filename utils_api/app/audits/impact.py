from typing import List, Optional
from app.schemas.organisation import OrganisationRecord
from app.schemas.analytics import AuditCheckItem, AuditDetails


def check_evidence_quality(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks the quality of evidence cited in impact claims.
    Pass if RCT/Meta-Analysis or Quasi-Experimental evidence is found.
    Warning if only lower forms of evidence are present.
    """
    base_details = AuditDetails(
        formula="Highest level of evidence cited in impact claims",
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_evidence_quality", status="null", significance="HIGH", category="Impact Awareness", details=base_details
    )

    if (
        not record.impact
        or not record.impact.importance_factors
        or not record.impact.importance_factors.problem_profile
        or record.impact.importance_factors.problem_profile.severity_dimensions is None
    ):
        base_item.details.calculation = "Impact data with severity dimensions is missing."
        return base_item

    evidence_levels = [dim.evidence_quality for dim in record.impact.importance_factors.problem_profile.severity_dimensions if dim.evidence_quality]

    if not evidence_levels:
        base_item.status = "warning"
        base_item.details.calculation = "No evidence quality was specified in any impact claim."
        return base_item

    highest_evidence = "None"
    order = ["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]
    for level in order:
        if level in evidence_levels:
            highest_evidence = level
            break

    base_item.details.calculation = f"Highest evidence found: '{highest_evidence}'."

    if highest_evidence in ["RCT/Meta-Analysis", "Quasi-Experimental"]:
        base_item.status = "pass"
    else:
        base_item.status = "warning"

    return base_item


def check_counterfactual_baseline(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks if a quantified counterfactual baseline is provided.
    Pass if description and value are populated.
    """
    base_details = AuditDetails(
        formula="Presence of a quantified counterfactual baseline",
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_counterfactual_baseline", status="null", significance="MEDIUM", category="Impact Awareness", details=base_details
    )

    if not record.impact or not record.impact.importance_factors or not record.impact.importance_factors.problem_profile or not record.impact.importance_factors.problem_profile.severity_dimensions:
        base_item.details.calculation = "Impact data with severity dimensions is missing."
        return base_item

    for dim in record.impact.importance_factors.problem_profile.severity_dimensions:
        if dim.counterfactual_baseline and dim.counterfactual_baseline.description and dim.counterfactual_baseline.value is not None:
            base_item.status = "pass"
            base_item.details.calculation = "A quantified counterfactual baseline was provided."
            return base_item

    base_item.status = "fail"
    base_item.details.calculation = "No quantified counterfactual baseline was provided."
    return base_item


def check_cost_per_outcome(record: OrganisationRecord) -> AuditCheckItem:
    """
    Calculates the cost per outcome. This is an informational check.
    """
    base_details = AuditDetails(
        formula="program_services_expenditure / primary_outcome_beneficiaries",
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_cost_per_outcome", status="null", significance="LOW", category="Impact Awareness", details=base_details
    )

    if not record.financials or not record.financials.expenditure or record.financials.expenditure.program_services is None:
        base_item.details.calculation = "Financials with program services expenditure are missing."
        return base_item

    program_spend = record.financials.expenditure.program_services
    
    if not record.impact or not record.impact.importance_factors:
        base_item.details.calculation = "Impact data is missing."
        return base_item

    populations = [b.population for b in record.impact.importance_factors.beneficiaries_demographic if b.population is not None]
    quant_values = [d.quantitative_data.value for d in record.impact.importance_factors.problem_profile.severity_dimensions if d.quantitative_data and d.quantitative_data.value is not None]
    
    all_outcomes = populations + quant_values
    if not all_outcomes:
        base_item.details.calculation = "No beneficiary population or quantitative outcome value found."
        return base_item

    primary_outcome = max(all_outcomes)

    if primary_outcome <= 0:
        base_item.details.calculation = f"Primary outcome value ({primary_outcome:g}) is not a positive number."
        return base_item

    cost_per = program_spend / primary_outcome
    base_item.details.calculation = f"(${program_spend:,.0f} / {primary_outcome:,.0f} beneficiaries) = ${cost_per:,.2f} per outcome"
    return base_item


def check_funding_neglectedness(record: OrganisationRecord) -> AuditCheckItem:
    """
    Calculates the ratio of government grants to total income.
    Warning if > 80% (low neglectedness), Pass if < 40% (high neglectedness).
    """
    base_details = AuditDetails(
        formula="government_grants / total_income",
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_funding_neglectedness", status="null", significance="MEDIUM", category="Impact Awareness", details=base_details
    )

    if not record.financials or not record.financials.income or record.financials.income.government_grants is None or record.financials.income.total is None:
        base_item.details.calculation = "Financials with income breakdown are missing."
        return base_item

    gov_grants, total_income = record.financials.income.government_grants, record.financials.income.total

    if total_income <= 0:
        base_item.details.calculation = f"Total income (${total_income:,.0f}) is not a positive number."
        return base_item

    ratio = gov_grants / total_income
    base_item.details.calculation = f"(${gov_grants:,.0f} / ${total_income:,.0f}) = {ratio:.1%}"

    if ratio > 0.8:
        base_item.status = "warning" # Low Neglectedness
    elif ratio < 0.4:
        base_item.status = "pass" # High Neglectedness
    else:
        base_item.status = "pass" # Medium Neglectedness, still a pass

    return base_item