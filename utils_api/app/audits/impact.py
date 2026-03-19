import json
from app.schemas.organisation import Metric, OrganisationRecord
from app.schemas.analytics import CheckItem, Details, CalculatedMetric
from app.schemas.custom_json_encoder import CustomEncoder
from typing import Optional
from app.audits.constants import INTERVENTION_LEVERAGE_MAP, EVIDENCE_HIERARCHY


def check_monitoring_and_evaluation(record: OrganisationRecord) -> CheckItem:
    """
    Checks the quality of self-reported evidence (M&E) in a charity's impact claims.
    This evaluates the organisation's capacity for rigorous self-assessment,
    independent of the general tractability of the interventions they perform.
    """
    base_details = Details(
        formula="Highest level of self-reported evidence cited in impact metrics",
        elaboration=None,
        calculation="Not computed",
    )
    base_item = CheckItem(
        id="check_monitoring_and_evaluation", status="warning", significance="MEDIUM", category="Impact Awareness", details=base_details
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

    evidence_levels = [metric.evidence_quality.value for metric in record.impact.metrics if metric.evidence_quality]

    if not any(evidence_levels):
        base_item.status = "warning"
        base_item.details.calculation = "No evidence quality was specified in any impact claim."
        return base_item

    highest_evidence = "None"
    highest_evidence_metric: Metric | None = None

    for level in EVIDENCE_HIERARCHY: # Find the highest evidence level present
        for metric in record.impact.metrics:
            if metric.evidence_quality.value == level:
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
    if highest_evidence_metric and highest_evidence_metric.source and highest_evidence_metric.source.quote:
        base_item.details.elaboration = f"Quote: '{highest_evidence_metric.source.quote}'"

    return base_item


def check_intervention_tractability(record: OrganisationRecord) -> CheckItem:
    """
    Evaluates the tractability of a charity's interventions by mapping them to
    Intervention Leverage Tiers (Systemic, Preventative, Direct). It aggregates
    all verified interventions into a portfolio for UI display.
    """
    base_details = Details(
        formula="Mapping of verified intervention types to the Intervention Leverage Tier framework.",
        elaboration=None,
        calculation="Not computed",
    )
    base_item = CheckItem(
        id="check_intervention_tractability", status="warning", significance="HIGH", category="Impact Awareness", details=base_details
    )

    if not record.impact or not record.impact.significant_events:
        base_item.details.calculation = "No significant events were reported to assess tractability."
        return base_item

    # 1. Filter for verified events and map them to tiers
    verified_interventions = []
    for event in record.impact.significant_events:
        if event.source and event.source.quote:
            for intervention_type in event.intervention_type:
                if intervention_type.value in INTERVENTION_LEVERAGE_MAP:
                    tier_info = INTERVENTION_LEVERAGE_MAP[intervention_type.value]
                    verified_interventions.append({
                        "name": intervention_type.value.replace('_', ' ').title(),
                        "tier": tier_info["tier"],
                        "tier_name": tier_info["tier_name"],
                        "source": event.source.model_dump(exclude_unset=True)
                    })

    if not verified_interventions:
        base_item.details.calculation = "No verifiable interventions found to assess tractability."
        return base_item

    # 2. Group by tier and determine the highest tier achieved
    highest_tier = 3
    highest_tier_name = "Tier 3: Direct Care & Indirect Action"
    portfolio_by_tier = {}
    for item in verified_interventions:
        if item["tier"] < highest_tier:
            highest_tier = item["tier"]
            highest_tier_name = item["tier_name"]

        if item["tier_name"] not in portfolio_by_tier:
            portfolio_by_tier[item["tier_name"]] = {"tier": item["tier"], "interventions": []}
        portfolio_by_tier[item["tier_name"]]["interventions"].append({"name": item["name"], "source": item["source"]})

    # 3. Format the portfolio for the 'elaboration' field
    # Sort tiers: Tier 1, Tier 2, Tier 3
    sorted_portfolio = sorted(portfolio_by_tier.items(), key=lambda x: x[1]['tier'])
    
    structured_portfolio = [{"tier_name": name, "interventions": data["interventions"]} for name, data in sorted_portfolio]
    base_item.details.elaboration = json.dumps(structured_portfolio, cls=CustomEncoder)

    # 4. Set calculation and status
    base_item.details.calculation = highest_tier_name
    if highest_tier in [1, 2]:
        base_item.status = "pass"
    else: # Tier 3 or no verifiable interventions
        base_item.status = "warning"

    return base_item


def check_counterfactual_baseline(record: OrganisationRecord) -> CheckItem:
    """
    Checks if a quantified counterfactual baseline is provided.
    Pass if description and value are populated.
    """
    base_details = Details(
        formula="Presence of a quantified counterfactual baseline", elaboration=None,
        calculation="Not computed",
    )
    base_item = CheckItem(
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
    """Calculates the cost per outcome with a confidence tier.

    The function follows a strict precedence:
    1) HIGH: Use explicitly stated unit costs (now an array) extracted from the charity's reporting.
    2) MEDIUM: Attempt to derive costs via programmatic spending breakdowns / pure-play logic.
    3) LOW: Abort for multi-domain organisations or when attribution is not possible.
    """

    if not record.impact or not record.impact.context:
        return None

    context = record.impact.context
    explicit_costs = context.explicit_unit_costs or []
    operating_scope = None
    if context.operating_scope and context.operating_scope.value:
        operating_scope = context.operating_scope.value.value

    def _to_usd(amount: float, currency: str | None) -> float:
        rate = 1.0
        if record.financials and record.financials.currency and record.financials.currency.usd_exchange_rate:
            rate = record.financials.currency.usd_exchange_rate
        if currency and record.financials and record.financials.currency and record.financials.currency.original_code:
            if currency.upper() == record.financials.currency.original_code.upper():
                rate = record.financials.currency.usd_exchange_rate or rate
        return amount * rate

    # --- HIGH CONFIDENCE ---
    explicit_results = []
    for cost in explicit_costs:
        if not cost or cost.amount is None:
            continue
        usd = _to_usd(cost.amount, cost.currency)
        explicit_results.append(
            {
                "intervention_type": cost.intervention_type.value
                if hasattr(cost.intervention_type, "value")
                else str(cost.intervention_type),
                "amount": cost.amount,
                "currency": cost.currency,
                "cost_usd": round(usd, 2),
            }
        )

    if explicit_results:
        calculation_string = (
            "Explicitly stated unit costs converted to USD: "
            + "; ".join(
                f"{r['intervention_type']}: {r['amount']:.2f} {r['currency']} -> ${r['cost_usd']:.2f}"
                for r in explicit_results
            )
        )

        return CalculatedMetric(
            id="cost_per_outcome",
            name="Cost Per Outcome (USD)",
            value=explicit_results,
            confidence_tier="HIGH",
            confidence_note="These unit costs are explicitly stated by the organisation in their reporting.",
            details={
                "formula": "Explicitly stated unit costs by the organisation.",
                "calculation": calculation_string,
            },
        )

    # --- LOW CONFIDENCE: Multi-domain organisations ---
    if operating_scope == "multi_domain_operations":
        return CalculatedMetric(
            id="cost_per_outcome",
            name="Cost Per Outcome (USD)",
            value=None,
            confidence_tier="LOW",
            confidence_note=(
                "Cost per outcome calculation is not available. This organisation conducts significant multi-domain work "
                "(e.g., human education, environmental conservation). Dividing the total budget solely by quantified animal outcomes "
                "would artificially inflate the cost and misrepresent their financial efficiency."
            ),
            details={
                "formula": "Calculation aborted due to multi-domain operations.",
                "calculation": "Not applicable.",
            },
        )

    # If the organisation is pure animal advocacy, but we lack the minimum data needed to
    # estimate a cost (e.g., programme spend or quantified beneficiaries), return None to
    # indicate that the metric cannot be computed rather than returning a LOW confidence value.
    if operating_scope == "pure_animal_advocacy":
        missing_spend = (
            not record.financials
            or not record.financials.expenditure
            or not record.financials.expenditure.program_services
            or record.financials.expenditure.program_services.value is None
        )
        missing_beneficiaries = not record.impact.beneficiaries
        if missing_spend or missing_beneficiaries:
            return None

    # --- MEDIUM CONFIDENCE: Programmatic matching via program_breakdowns ---
    has_breakdowns = bool(
        record.financials
        and record.financials.expenditure
        and record.financials.expenditure.program_breakdowns
    )

    if (
        has_breakdowns
        and record.impact.significant_events
        and record.impact.beneficiaries
    ):
        # Map intervention types to beneficiary types for population allocation
        intervention_to_beneficiary = {
            "high_volume_spay_neuter": "companion_animals",
            "individual_rescue_and_sanctuary": "companion_animals",
            "veterinary_care_and_treatment": "companion_animals",
            "wildlife_conservation_and_habitat_protection": "wild_animals",
            "corporate_welfare_campaigns": "farmed_animals",
            "policy_and_legal_advocacy": "farmed_animals",
            "alternative_protein_and_food_tech": "farmed_animals",
            "vegan_outreach_and_dietary_change": "farmed_animals",
            # Fallbacks for broad/indirect interventions
            "scientific_and_welfare_research": "unspecified",
            "capacity_building_and_movement_growth": "unspecified",
            "undercover_investigations_and_exposes": "unspecified",
            "disaster_response_and_emergency_relief": "unspecified",
            "humane_education_and_community_support": "unspecified",
        }

        def _population_for_interventions(interventions: list[str]) -> float:
            target_types = {
                intervention_to_beneficiary.get(i)
                for i in interventions
                if intervention_to_beneficiary.get(i)
            }
            return sum(
                b.population
                for b in record.impact.beneficiaries
                if b.beneficiary_type.value in target_types and b.population
            )

        program_matches = []
        for breakdown in record.financials.expenditure.program_breakdowns:
            if not breakdown or not breakdown.programme_name or not breakdown.amount or breakdown.amount.value is None:
                continue

            name_lower = breakdown.programme_name.lower()
            matched_event = None
            for event in record.impact.significant_events:
                if not event or not event.event_name:
                    continue
                if (
                    name_lower in event.event_name.lower()
                    or event.event_name.lower() in name_lower
                    or (event.summary and name_lower in event.summary.lower())
                    or (event.summary and event.summary.lower() in name_lower)
                ):
                    matched_event = event
                    break

            if not matched_event:
                continue

            population = _population_for_interventions(
                [it.value if hasattr(it, "value") else it for it in (matched_event.intervention_type or [])]
            )
            if population <= 0:
                continue

            cost_usd = _to_usd(breakdown.amount.value, None) / population
            program_matches.append(
                {
                    "programme_name": breakdown.programme_name,
                    "matched_event": matched_event.event_name,
                    "intervention_types": [
                        it.value if hasattr(it, "value") else it
                        for it in (matched_event.intervention_type or [])
                    ],
                    "population": population,
                    "cost_usd": round(cost_usd, 2),
                }
            )

        if program_matches:
            calculation_string = (
                "Programmatic spend was matched to reported interventions; costs were derived per matching beneficiary population."
            )
            return CalculatedMetric(
                id="cost_per_outcome",
                name="Cost Per Outcome (USD)",
                value=program_matches,
                confidence_tier="MEDIUM",
                confidence_note=(
                    "Derived from program_breakdowns matched to significant events and their beneficiary populations."
                ),
                details={
                    "formula": "matched_program_breakdown_spend / beneficiary_population",
                    "calculation": calculation_string,
                },
            )

    # --- MEDIUM CONFIDENCE: Pure-Play cohort benchmark / fallback ---
    if (
        operating_scope == "pure_animal_advocacy"
        and record.financials
        and record.financials.expenditure
        and record.financials.expenditure.program_services
        and record.impact.beneficiaries
        and record.financials.expenditure.program_services.value is not None
    ):
        program_spend = record.financials.expenditure.program_services.value
        rate = (
            record.financials.currency.usd_exchange_rate
            if record.financials.currency and record.financials.currency.usd_exchange_rate
            else 1.0
        )

        total_population = sum(
            b.population for b in record.impact.beneficiaries if b.population
        )
        if total_population <= 0:
            return None

        cost_per_usd = (program_spend * rate) / total_population
        calculation_string = (
            f"(${program_spend * rate:,.0f} USD / {total_population:,.0f} total beneficiaries) = ${cost_per_usd:,.2f} USD per outcome"
        )

        if cost_per_usd > 0:
            outcomes_per_1000 = 1000 / cost_per_usd
            outcomes_str = f"{outcomes_per_1000:,.0f}" if outcomes_per_1000 >= 1 else f"{outcomes_per_1000:.3g}"
            calculation_string += f". | A $1,000 USD donation achieves ≈ {outcomes_str} outcomes."

        confidence_note = (
            "This unit cost is estimated by PRISM by dividing total programme expenditure by the total quantified animal beneficiaries."
        )

        # If breakdown data exists, attempt to use pure-play logic
        if has_breakdowns:
            breakdown_values = [
                b.amount.value
                for b in record.financials.expenditure.program_breakdowns
                if b and b.amount and b.amount.value is not None
            ]
            if breakdown_values and program_spend > 0:
                max_breakdown = max(breakdown_values)
                if max_breakdown / program_spend >= 0.8:
                    confidence_note = (
                        "Pure-Play benchmark: >80% of program services spend is attributed to a single programme."
                    )

        return CalculatedMetric(
            id="cost_per_outcome",
            name="Cost Per Outcome (USD)",
            value=round(cost_per_usd, 2),
            confidence_tier="MEDIUM",
            confidence_note=confidence_note,
            details={
                "formula": "program_services_expenditure / sum_of_beneficiaries",
                "calculation": calculation_string,
            },
        )

    return CalculatedMetric(
        id="cost_per_outcome",
        name="Cost Per Outcome (USD)",
        value=None,
        confidence_tier="LOW",
        confidence_note="Calculation could not be performed due to missing data (e.g., operating scope, financials, or beneficiaries).",
        details={"formula": "Not applicable.", "calculation": "Not applicable."},
    )


def check_funding_neglectedness(record: OrganisationRecord) -> CheckItem:
    """
    Calculates the ratio of government grants to total income.
    Warning if > 80% (low neglectedness), Pass if < 40% (high neglectedness).
    """
    base_details = Details(
        formula="government_grants / total_income", elaboration=None,
        calculation="Not computed",
    )
    base_item = CheckItem(
        id="check_funding_neglectedness", status="warning", significance="MEDIUM", category="Impact Awareness", details=base_details
    )

    if (
        not record.financials
        or not record.financials.income
        or not record.financials.income.government_grants
        or record.financials.income.government_grants.value is None
        or not record.financials.income.total
        or record.financials.income.total.value is None
    ):
        base_item.details.calculation = "Financials with income breakdown are missing."
        return base_item

    gov_grants = record.financials.income.government_grants.value
    total_income = record.financials.income.total.value

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


def check_cause_area_neglectedness(record: OrganisationRecord) -> CheckItem:
    """
    Checks the neglectedness of the charity's cause area based on beneficiary type.
    If population data is available, it calculates the proportion of high-neglectedness
    beneficiaries ('farmed_animals', 'wild_animals').
    - >= 50% high-neglectedness -> pass
    - > 0% and < 50% high-neglectedness -> warning
    - 100% low-neglectedness ('companion_animals') -> warning
    If population data is missing, it falls back to presence-based logic.
    """
    base_details = Details(
        formula="Proportional analysis of beneficiary populations (farmed/wild vs. companion)", elaboration=None,
        calculation="Not computed",
    )
    base_item = CheckItem(
        id="check_cause_area_neglectedness", status="warning", significance="HIGH", category="Impact Awareness", details=base_details
    )

    if not record.impact or not record.impact.beneficiaries:
        base_item.status = "warning"
        base_item.details.calculation = "Impact data with beneficiary types is missing."
        return base_item

    populations = {
        "farmed_animals": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type.value == "farmed_animals" and b.population),
        "wild_animals": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type.value == "wild_animals" and b.population),
        "companion_animals": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type.value == "companion_animals" and b.population),
        "unspecified": sum(b.population for b in record.impact.beneficiaries if b.beneficiary_type.value == "unspecified" and b.population),
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
    beneficiary_types = {b.beneficiary_type.value for b in record.impact.beneficiaries if b.beneficiary_type}
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