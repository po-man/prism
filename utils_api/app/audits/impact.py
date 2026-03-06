from app.schemas.organisation import Metric, OrganisationRecord
from app.schemas.analytics import AuditCheckItem, AuditDetails, CalculatedMetric
from typing import Optional


def check_evidence_quality(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks the quality of evidence cited in impact claims.
    Pass if RCT/Meta-Analysis or Quasi-Experimental evidence is found.
    Warning if only lower forms of evidence are present.
    """
    base_details = AuditDetails(
        formula="Highest level of evidence cited in impact claims",
        elaboration=None,
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_evidence_quality", status="warning", significance="HIGH", category="Impact Awareness", details=base_details
    )

    if not record.impact:
        base_item.details.calculation = "Impact data with metrics is missing."
        return base_item

    # Now we know record.impact exists. Check for metrics.
    if not record.impact.metrics:
        # This case is different from no evidence *specified*. It means there are no impact claims at all.
        base_item.status = "warning"
        base_item.details.calculation = "No impact metrics were provided to assess evidence quality."
        return base_item

    evidence_levels = [metric.evidence_quality for metric in record.impact.metrics if metric.evidence_quality]

    if not any(evidence_levels):
        base_item.status = "warning"
        base_item.details.calculation = "No evidence quality was specified in any impact claim."
        return base_item

    highest_evidence = "None"
    highest_evidence_metric: Metric | None = None
    order = ["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]

    for level in order: # Find the highest evidence level present
        for metric in record.impact.metrics:
            if metric.evidence_quality == level:
                highest_evidence = level
                highest_evidence_metric = metric
                break
        if highest_evidence_metric:
            break # Found the highest, stop searching

    base_item.details.calculation = f"Highest evidence found: '{highest_evidence}'."

    if highest_evidence in ["RCT/Meta-Analysis", "Quasi-Experimental"]:
        base_item.status = "pass"
    else:
        base_item.status = "warning"
    if highest_evidence_metric and highest_evidence_metric.evidence_quote:
        base_item.details.elaboration = f"Quote: '{highest_evidence_metric.evidence_quote}'"

    return base_item


def check_counterfactual_baseline(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks if a quantified counterfactual baseline is provided.
    Pass if description and value are populated.
    """
    base_details = AuditDetails(
        formula="Presence of a quantified counterfactual baseline", elaboration=None,
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_counterfactual_baseline", status="fail", significance="MEDIUM", category="Impact Awareness", details=base_details
    )

    if not record.impact or not record.impact.metrics:
        base_item.details.calculation = "Impact data with metrics is missing."
        return base_item

    for metric in record.impact.metrics:
        if metric.counterfactual_baseline and metric.counterfactual_baseline.description and metric.counterfactual_baseline.value is not None:
            base_item.status = "pass"
            base_item.details.calculation = "A quantified counterfactual baseline was provided."
            return base_item

    base_item.status = "fail"
    base_item.details.calculation = "No quantified counterfactual baseline was provided."
    return base_item


def calculate_cost_per_outcome(record: OrganisationRecord) -> Optional[CalculatedMetric]:
    """
    Calculates the cost per outcome. This is an informational check.
    """
    if (
        not record.financials
        or not record.financials.expenditure
        or record.financials.expenditure.program_services is None
    ):
        return None

    program_spend = record.financials.expenditure.program_services
    # Fetch the exchange rate, defaulting to 1.0 if not present
    rate = (
        record.financials.currency.usd_exchange_rate if record.financials.currency and record.financials.currency.usd_exchange_rate else 1.0
    )
    program_spend_usd = program_spend * rate

    if not record.impact or not record.impact.beneficiaries:
        return None

    primary_outcome = sum([b.population for b in record.impact.beneficiaries if b.population is not None])

    if primary_outcome <= 0:
        return None

    cost_per_usd = program_spend_usd / primary_outcome
    calculation_string = f"(${program_spend_usd:,.0f} USD / {primary_outcome:,.0f} total beneficiaries) = ${cost_per_usd:,.2f} USD per outcome"

    # Add a secondary metric for the UI myth-buster section
    if cost_per_usd > 0:
        outcomes_per_1000 = 1000 / cost_per_usd
        calculation_string += f". | A $1,000 USD donation achieves ≈ {outcomes_per_1000:.3g} outcomes."

    return CalculatedMetric(
        id="cost_per_outcome",
        name="Cost Per Outcome (USD)",
        value=round(cost_per_usd, 2),
        details={
            "formula": "program_services_expenditure / sum_of_beneficiaries",
            "calculation": calculation_string,
        },
    )


def check_funding_neglectedness(record: OrganisationRecord) -> AuditCheckItem:
    """
    Calculates the ratio of government grants to total income.
    Warning if > 80% (low neglectedness), Pass if < 40% (high neglectedness).
    """
    base_details = AuditDetails(
        formula="government_grants / total_income", elaboration=None,
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_funding_neglectedness", status="warning", significance="MEDIUM", category="Impact Awareness", details=base_details
    )

    if not record.financials or not record.financials.income or record.financials.income.government_grants is None or record.financials.income.total is None:
        base_item.details.calculation = "Financials with income breakdown are missing."
        return base_item

    gov_grants, total_income = record.financials.income.government_grants, record.financials.income.total

    if total_income <= 0:
        base_item.details.calculation = f"Total income (${total_income:,.0f}) is not a positive number."
        base_item.status = "warning"
        return base_item

    ratio = gov_grants / total_income
    base_item.details.calculation = f"(${gov_grants:,.0f} / ${total_income:,.0f}) = {ratio:.1%}"

    if ratio > 0.8:
        base_item.status = "fail" # Low Neglectedness
    elif ratio < 0.4:
        base_item.status = "pass" # High Neglectedness
    else:
        base_item.status = "pass" # Medium Neglectedness, still a pass

    return base_item


def check_cause_area_neglectedness(record: OrganisationRecord) -> AuditCheckItem:
    """
    Checks the neglectedness of the charity's cause area based on beneficiary type.
    If population data is available, it calculates the proportion of high-neglectedness
    beneficiaries ('farmed_animals', 'wild_animals').
    - >= 50% high-neglectedness -> pass
    - > 0% and < 50% high-neglectedness -> warning
    - 100% low-neglectedness ('companion_animals') -> warning
    If population data is missing, it falls back to presence-based logic.
    """
    base_details = AuditDetails(
        formula="Proportional analysis of beneficiary populations (farmed/wild vs. companion)", elaboration=None,
        calculation="Not computed",
    )
    base_item = AuditCheckItem(
        id="check_cause_area_neglectedness", status="warning", significance="HIGH", category="Impact Awareness", details=base_details
    )

    if not record.impact or not record.impact.beneficiaries:
        base_item.status = "warning"
        base_item.details.calculation = "Impact data with beneficiary types is missing."
        return base_item

    populations = {
        "farmed_animals": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type == "farmed_animals" and b.population),
        "wild_animals": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type == "wild_animals" and b.population),
        "companion_animals": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type == "companion_animals" and b.population),
    }
    total_population = sum(populations.values())

    # If population data exists, use proportional logic
    if total_population > 0:
        high_neglectedness_pop = populations["farmed_animals"] + populations["wild_animals"]
        high_neglectedness_ratio = high_neglectedness_pop / total_population

        percentages = {k: (v / total_population * 100) for k, v in populations.items() if v > 0}
        breakdown = ", ".join([f"{k.replace('_', ' ').title()}: {v:.0f}%" for k, v in percentages.items()])

        if high_neglectedness_ratio >= 0.5:
            base_item.status = "pass"
            base_item.details.calculation = f"Focus on high-neglectedness areas ({breakdown})."
        elif high_neglectedness_ratio > 0:
            base_item.status = "warning"
            base_item.details.calculation = f"Mixed portfolio with minority focus on high-neglectedness areas ({breakdown})."
        else: # high_neglectedness_ratio is 0
            base_item.status = "fail"
            base_item.details.calculation = f"Operates in a low-neglectedness / saturated area ({breakdown})."
        return base_item

    # Fallback to presence-based logic if no population data
    beneficiary_types = {b.beneficiary_type for b in record.impact.beneficiaries if b.beneficiary_type}
    base_item.details.formula = "Evaluation of beneficiary_type presence against EA principles for animal advocacy"

    high_neglectedness = {"farmed_animals", "wild_animals"}
    low_neglectedness = {"companion_animals"}

    high_neglectedness_found = beneficiary_types.intersection(high_neglectedness)
    if high_neglectedness_found:
        base_item.status = "pass"
        base_item.details.calculation = f"Operates in high-neglectedness area(s): {', '.join(high_neglectedness_found)}. Population data not available for proportional analysis."
    elif beneficiary_types.issubset(low_neglectedness):
        base_item.status = "warning"
        base_item.details.calculation = "Operates in a low-neglectedness / saturated area (companion animals). Population data not available for proportional analysis."
    else:
        base_item.details.calculation = "No beneficiary types were specified."

    return base_item