from copy import deepcopy
import json
from fastapi.testclient import TestClient

# A valid base record to ensure requests pass Pydantic validation.
from tests.shared import VALID_BASE_RECORD


def get_audit_item(response_json: dict, item_id: str):
    """Helper to find a specific audit check item in the response."""
    return next((item for item in response_json["check_items"] if item["id"] == item_id), None)


def get_calculated_metric(response_json: dict, metric_id: str):
    """Helper to find a specific calculated metric in the response."""
    return next((metric for metric in response_json["calculated_metrics"] if metric["id"] == metric_id), None)


def test_check_monitoring_and_evaluation(client: TestClient):
    """Tests the check_monitoring_and_evaluation audit for various evidence levels."""
    # 1. Pass with high-quality evidence
    record_high_evidence = deepcopy(VALID_BASE_RECORD)
    record_high_evidence["impact"]["metrics"]["metrics"][0]["evidence_quality"] = "Quasi-Experimental"
    record_high_evidence["impact"]["metrics"]["metrics"][0]["source"]["quote"] = "We saw a 50% increase."
    response = client.post("/audit", json=record_high_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_monitoring_and_evaluation")
    assert item["status"] == "pass"
    assert item["details"]["calculation"] == "Highest evidence found: 'Quasi-Experimental'."
    assert item["details"]["elaboration"] == "Quote: 'We saw a 50% increase.'"

    # 2. Warning with only low-quality evidence
    record_low_evidence = deepcopy(VALID_BASE_RECORD)
    record_low_evidence["impact"]["metrics"]["metrics"][0]["evidence_quality"] = "Pre-Post"
    record_low_evidence["impact"]["metrics"]["metrics"][0]["source"]["quote"] = None # Explicitly remove for this test
    response = client.post("/audit", json=record_low_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_monitoring_and_evaluation")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "Highest evidence found: 'Pre-Post'."
    assert item["details"]["elaboration"] is None # No quote in base record

    # 3. Warning when no evidence is specified
    record_no_evidence = deepcopy(VALID_BASE_RECORD)
    record_no_evidence["impact"]["metrics"]["metrics"] = []
    response = client.post("/audit", json=record_no_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_monitoring_and_evaluation")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "No impact metrics were provided to assess evidence quality."

    # 4. Default status with missing impact data
    record_missing_impact = deepcopy(VALID_BASE_RECORD)
    del record_missing_impact["impact"]
    response = client.post("/audit", json=record_missing_impact)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_monitoring_and_evaluation")
    assert item["details"]["calculation"] == "Impact data with metrics is missing."


def test_check_intervention_tractability(client: TestClient):
    """Tests the check_intervention_tractability audit for the new Leverage Tier mappings."""
    # 1. Pass: A mix of Tier 1 and Tier 3 interventions should result in a 'pass' and a Tier 1 calculation.
    record_tier1 = deepcopy(VALID_BASE_RECORD)
    record_tier1["impact"]["interventions"]["significant_events"] = [
        {
            "event_name": "Rescue Operation",
            "summary": "Rescued animals.",
            "intervention_type": ["individual_rescue_and_sanctuary"], # Tier 3
            "intervention_type_other_description": None,
            "timeframe": "annual",
            "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "We rescued animals.", "resolved_url": None}
        },
        {
            "event_name": "Corporate Campaign",
            "summary": "Caged-free campaign.",
            "intervention_type": ["corporate_welfare_campaigns"], # Tier 1
            "intervention_type_other_description": None,
            "timeframe": "annual",
            "source": {"source_type": "attached_report", "source_index": 0, "page_number": 2, "search_result_index": None, "quote": "Our campaign was successful.", "resolved_url": None}
        }
    ]
    response = client.post("/audit", json=record_tier1)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_intervention_tractability")
    assert item["status"] == "pass"
    assert item["details"]["calculation"] == "Tier 1: Systemic Change"
    
    # Assert the elaboration contains a structured, parseable JSON portfolio
    portfolio = json.loads(item["details"]["elaboration"])
    assert len(portfolio) == 2 # One for each tier
    assert portfolio[0]["tier_name"] == "Tier 1: Systemic Change"
    assert portfolio[0]["interventions"][0]["name"] == "Corporate Welfare Campaigns"
    assert portfolio[1]["tier_name"] == "Tier 3: Direct Care & Indirect Action"
    assert portfolio[1]["interventions"][0]["name"] == "Individual Rescue And Sanctuary"

    # 2. Warning: Only Tier 3 interventions should result in a 'warning'.
    record_tier3 = deepcopy(VALID_BASE_RECORD)
    record_tier3["impact"]["interventions"]["significant_events"] = [
        {
            "event_name": "Vet Care",
            "summary": "Provided vet care.",
            "intervention_type": ["veterinary_care_and_treatment"], # Tier 3
            "intervention_type_other_description": None,
            "timeframe": "annual",
            "source": {"source_type": "attached_report", "source_index": 0, "page_number": 3, "search_result_index": None, "quote": "We did a mixed event.", "resolved_url": None}
        }
    ]
    response = client.post("/audit", json=record_tier3)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_intervention_tractability")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "Tier 3: Direct Care & Indirect Action"
    portfolio = json.loads(item["details"]["elaboration"])
    assert len(portfolio) == 1
    assert portfolio[0]["tier_name"] == "Tier 3: Direct Care & Indirect Action"

    # 3. Warning: No significant events reported
    record_no_events = deepcopy(VALID_BASE_RECORD)
    record_no_events["impact"]["interventions"]["significant_events"] = []
    response = client.post("/audit", json=record_no_events)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_intervention_tractability")
    assert item["status"] == "warning" # The default status is warning
    assert item["details"]["calculation"] == "No significant events were reported to assess tractability."
    assert item["details"]["elaboration"] is None

    # 4. Warning: No impact data at all
    record_no_impact = deepcopy(VALID_BASE_RECORD)
    del record_no_impact["impact"]
    response = client.post("/audit", json=record_no_impact)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_intervention_tractability")
    assert item["status"] == "warning" # The default status is warning
    assert item["details"]["calculation"] == "No significant events were reported to assess tractability."


def test_check_counterfactual_baseline(client: TestClient):
    """Tests the check_counterfactual_baseline audit."""

    # 1. Pass when a quantified baseline is present
    record_pass = deepcopy(VALID_BASE_RECORD)
    response = client.post("/audit", json=record_pass)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_counterfactual_baseline")
    assert item["status"] == "pass"
    assert item["details"]["calculation"] == "A quantified counterfactual baseline was provided."

    # 2. Fail when baseline is missing value
    record_no_value = deepcopy(VALID_BASE_RECORD)
    record_no_value["impact"]["metrics"]["metrics"][0]["counterfactual_baseline"]["value"] = None
    response = client.post("/audit", json=record_no_value)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_counterfactual_baseline")
    assert item["status"] == "fail"
    assert item["details"]["calculation"] == "No quantified counterfactual baseline was provided."

    # 3. Default status with missing impact data
    record_missing_impact = deepcopy(VALID_BASE_RECORD)
    del record_missing_impact["impact"]
    response = client.post("/audit", json=record_missing_impact)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_counterfactual_baseline")
    assert item["details"]["calculation"] == "Impact data with metrics is missing."


def test_calculate_cost_per_outcome_confidence_tiers(client: TestClient):
    """Tests the calculate_cost_per_outcome metric for HIGH, MEDIUM, and LOW confidence scenarios."""

    # 1. HIGH confidence: Explicit unit cost is provided
    record_high = deepcopy(VALID_BASE_RECORD)
    record_high["impact"]["interventions"]["context"]["explicit_unit_costs"] = [
        {
            "intervention_type": "high_volume_spay_neuter",
            "amount": 25,
            "currency": "HKD",
            "description": "Cost to spay one dog.",
            "source": {
                "source_type": "attached_report",
                "source_index": 0,
                "page_number": 18,
                "search_result_index": None,
                "quote": "It costs just $25 to spay one dog.",
                "resolved_url": None
            }
        }
    ]
    # Base record has HKD rate of 0.128. 25 * 0.128 = 3.2
    response = client.post("/audit", json=record_high)
    assert response.status_code == 200, response.text
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item["confidence_tier"] == "HIGH"
    assert isinstance(item["value"], list)
    assert item["value"][0]["intervention_type"] == "high_volume_spay_neuter"
    assert item["value"][0]["cost_usd"] == 3.2
    assert "explicitly stated unit costs converted to usd" in item["details"]["calculation"].lower()

    # 2. MEDIUM confidence: Pure animal advocacy, PRISM calculates
    record_medium = deepcopy(VALID_BASE_RECORD)
    record_medium["impact"]["interventions"]["context"]["operating_scope"] = {"value": "pure_animal_advocacy", "source": {"source_type": "web_search", "source_index": None, "page_number": None, "search_result_index": 0, "quote": "We are an organisation dedicated to animal advocacy.", "resolved_url": None}}
    record_medium["impact"]["interventions"]["context"]["explicit_unit_costs"] = []
    record_medium["financials"]["expenditure"]["program_services"]["value"] = 400000 # HKD
    record_medium["financials"]["currency"]["usd_exchange_rate"] = 0.1 # Simple rate
    record_medium["impact"]["beneficiaries"]["beneficiaries"] = [{"location": "HK", "population": 500, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}}]
    # Program spend USD = 400,000 * 0.1 = 40,000
    # Beneficiaries = 500
    # Cost per outcome = 40,000 / 500 = 80
    response = client.post("/audit", json=record_medium)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item["confidence_tier"] == "MEDIUM"
    assert item["value"] == 80.0
    assert "estimated by PRISM" in item["confidence_note"]
    assert "($40,000 USD / 500 total beneficiaries) = $80.00 USD per outcome" in item["details"]["calculation"]

    # 3. MEDIUM confidence: Programmatic matching from program_breakdowns to significant events
    record_programmatic = deepcopy(VALID_BASE_RECORD)
    record_programmatic["impact"]["interventions"]["context"]["operating_scope"] = {"value": "pure_animal_advocacy", "source": {"source_type": "web_search", "source_index": None, "page_number": None, "search_result_index": 0, "quote": "We are an organisation dedicated to animal advocacy.", "resolved_url": None}}
    record_programmatic["impact"]["interventions"]["context"]["explicit_unit_costs"] = []
    record_programmatic["impact"]["interventions"]["significant_events"] = [
        {
            "event_name": "Mobile Spay Clinic Operations",
            "summary": "Ran mobile spay clinics.",
            "intervention_type": ["high_volume_spay_neuter"],
            "intervention_type_other_description": None,
            "timeframe": "annual",
            "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "We ran mobile spay clinics.", "resolved_url": None}
        }
    ]
    record_programmatic["impact"]["beneficiaries"]["beneficiaries"] = [{"location": "HK", "population": 1000, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "Helped 1000 animals.", "resolved_url": None}}]
    record_programmatic["financials"]["expenditure"]["program_breakdowns"] = [{"programme_name": "Mobile Spay Clinic Operations", "amount": {"value": 100000, "source": {"source_type": "attached_report", "source_index": 0, "page_number": 2, "search_result_index": None, "quote": "Mobile spay clinic ops cost 100,000.", "resolved_url": None}}}]
    record_programmatic["financials"]["currency"]["usd_exchange_rate"] = 0.1
    response = client.post("/audit", json=record_programmatic)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item["confidence_tier"] == "MEDIUM"
    assert isinstance(item["value"], list)
    assert item["value"][0]["programme_name"] == "Mobile Spay Clinic Operations"
    assert item["value"][0]["cost_usd"] == 10.0

    # 4. MEDIUM confidence: Pure-play cohort benchmark
    record_pure_play = deepcopy(VALID_BASE_RECORD)
    record_pure_play["impact"]["interventions"]["context"]["operating_scope"] = {"value": "pure_animal_advocacy", "source": {"source_type": "web_search", "source_index": None, "page_number": None, "search_result_index": 0, "quote": "We are an organisation dedicated to animal advocacy.", "resolved_url": None}}
    record_pure_play["impact"]["interventions"]["context"]["explicit_unit_costs"] = []
    record_pure_play["impact"]["beneficiaries"]["beneficiaries"] = [{"location": "HK", "population": 1000, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "Helped 1000 animals.", "resolved_url": None}}]
    record_pure_play["financials"]["expenditure"]["program_services"]["value"] = 100000
    record_pure_play["financials"]["currency"]["usd_exchange_rate"] = 0.1
    record_pure_play["financials"]["expenditure"]["program_breakdowns"] = [
        {"programme_name": "Primary Programme", "amount": {"value": 90000, "source": {"source_type": "attached_report", "source_index": 0, "page_number": 2, "search_result_index": None, "quote": "Primary programme spend.", "resolved_url": None}}},
        {"programme_name": "Secondary Programme", "amount": {"value": 10000, "source": {"source_type": "attached_report", "source_index": 0, "page_number": 3, "search_result_index": None, "quote": "Secondary programme spend.", "resolved_url": None}}}
    ]
    response = client.post("/audit", json=record_pure_play)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item["confidence_tier"] == "MEDIUM"
    assert item["value"] == 10.0
    assert "Pure-Play" in item["confidence_note"]

    # 5. LOW confidence: Multi-domain operations, calculation is aborted
    record_low_multidomain = deepcopy(VALID_BASE_RECORD)
    record_low_multidomain["impact"]["interventions"]["context"]["operating_scope"] = {"value": "multi_domain_operations", "source": {"source_type": "web_search", "source_index": None, "page_number": None, "search_result_index": 0, "quote": "We are an organisation dedicated to animal advocacy.", "resolved_url": None}}
    record_low_multidomain["impact"]["interventions"]["context"]["explicit_unit_costs"] = []
    response = client.post("/audit", json=record_low_multidomain)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item["confidence_tier"] == "LOW"
    assert item["value"] is None
    assert "multi-domain work" in item["confidence_note"]
    assert item["details"]["formula"] == "Calculation aborted due to multi-domain operations."

    # 6. No metric calculated: Missing essential data for MEDIUM calculation
    record_medium_fail = deepcopy(VALID_BASE_RECORD)
    record_medium_fail["impact"]["interventions"]["context"]["operating_scope"] = {"value": "pure_animal_advocacy", "source": {"source_type": "web_search", "source_index": None, "page_number": None, "search_result_index": 0, "quote": "We are an organisation dedicated to animal advocacy.", "resolved_url": None}}
    record_medium_fail["impact"]["interventions"]["context"]["explicit_unit_costs"] = []
    record_medium_fail["financials"]["expenditure"]["program_services"]["value"] = None # Missing spend
    response = client.post("/audit", json=record_medium_fail)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item is None # Function should return None, not a LOW confidence metric

    # 7. No metric calculated: Beneficiary population is zero
    record_zero_beneficiaries = deepcopy(VALID_BASE_RECORD)
    record_zero_beneficiaries["impact"]["interventions"]["context"]["operating_scope"] = {"value": "pure_animal_advocacy", "source": {"source_type": "web_search", "source_index": None, "page_number": None, "search_result_index": 0, "quote": "We are an organisation dedicated to animal advocacy.", "resolved_url": None}}
    record_zero_beneficiaries["impact"]["interventions"]["context"]["explicit_unit_costs"] = []
    record_zero_beneficiaries["impact"]["beneficiaries"]["beneficiaries"] = [{"location": "HK", "population": 0, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}}]
    response = client.post("/audit", json=record_zero_beneficiaries)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item is None # Cannot divide by zero

    # 8. MEDIUM confidence: Handles zero program spend correctly
    record_zero_spend = deepcopy(VALID_BASE_RECORD)
    record_zero_spend["impact"]["interventions"]["context"]["operating_scope"] = {"value": "pure_animal_advocacy", "source": {"source_type": "web_search", "source_index": None, "page_number": None, "search_result_index": 0, "quote": "We are an organisation dedicated to animal advocacy.", "resolved_url": None}}
    record_zero_spend["impact"]["interventions"]["context"]["explicit_unit_costs"] = []
    record_zero_spend["financials"]["expenditure"]["program_services"]["value"] = 0
    record_zero_spend["impact"]["beneficiaries"]["beneficiaries"] = [{"location": "HK", "population": 500, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}}]
    response = client.post("/audit", json=record_zero_spend)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item["confidence_tier"] == "MEDIUM"
    assert item["value"] == 0.0
    assert "($0 USD / 500 total beneficiaries) = $0.00 USD per outcome" in item["details"]["calculation"]


def test_check_funding_neglectedness(client: TestClient):
    """Tests the check_funding_neglectedness audit."""

    # 1. Pass for medium neglectedness (between 40% and 80% inclusive)
    record_medium = deepcopy(VALID_BASE_RECORD)
    record_medium["financials"]["income"]["total"]["value"] = 1000000
    record_medium["financials"]["income"]["government_grants"]["value"] = 500000 # 50%
    response = client.post("/audit", json=record_medium)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["status"] == "pass"
    assert "50.0%" in item["details"]["calculation"]

    # 2. Pass for high neglectedness (< 40%)
    record_high = deepcopy(VALID_BASE_RECORD)
    record_high["financials"]["income"]["total"]["value"] = 1000000
    record_high["financials"]["income"]["government_grants"]["value"] = 200000 # 20%
    response = client.post("/audit", json=record_high)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["status"] == "pass"
    assert "20.0%" in item["details"]["calculation"]

    # 3. Fail for low neglectedness (> 80%)
    record_low = deepcopy(VALID_BASE_RECORD)
    record_low["financials"]["income"]["total"]["value"] = 1000000
    record_low["financials"]["income"]["government_grants"]["value"] = 850000 # 85%
    response = client.post("/audit", json=record_low)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["status"] == "fail"
    assert "85.0%" in item["details"]["calculation"]

    # 4. Handles zero total income
    record_zero_income = deepcopy(VALID_BASE_RECORD)
    record_zero_income["financials"]["income"]["total"]["value"] = 0
    response = client.post("/audit", json=record_zero_income)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert "is not a positive number" in item["details"]["calculation"]

    # 5. Default status for missing financial data
    record_missing_financials = deepcopy(VALID_BASE_RECORD)
    del record_missing_financials["financials"]
    response = client.post("/audit", json=record_missing_financials)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["details"]["calculation"] == "Financials with income breakdown are missing."


def test_check_cause_area_neglectedness(client: TestClient):
    """Tests the check_cause_area_neglectedness audit for animal advocacy."""

    # 1. Pass for >= 50% high-neglectedness population
    record_pass = deepcopy(VALID_BASE_RECORD)
    record_pass["impact"]["beneficiaries"]["beneficiaries"] = [
        {"location": "HK", "population": 800, "beneficiary_type": "wild_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}},
        {"location": "HK", "population": 200, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}},
    ]
    response = client.post("/audit", json=record_pass)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "pass"
    assert item["details"]["calculation"] == "Focus on high-neglectedness areas (Wild Animals: 80%, Companion Animals: 20%)."

    # 2. Warning for < 50% high-neglectedness population
    record_warning_mixed = deepcopy(VALID_BASE_RECORD)
    record_warning_mixed["impact"]["beneficiaries"]["beneficiaries"] = [
        {"location": "HK", "population": 150, "beneficiary_type": "farmed_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}},
        {"location": "HK", "population": 850, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}},
    ]
    response = client.post("/audit", json=record_warning_mixed)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "Mixed portfolio with minority focus on high-neglectedness areas (Farmed Animals: 15%, Companion Animals: 85%)."

    # 3. Fail for 100% low-neglectedness population
    record_warning_low = deepcopy(VALID_BASE_RECORD)
    record_warning_low["impact"]["beneficiaries"]["beneficiaries"] = [
        {"location": "HK", "population": 1000, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}}
    ]
    response = client.post("/audit", json=record_warning_low)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "fail"
    assert item["details"]["calculation"] == "Operates in a low-neglectedness / saturated area (Companion Animals: 100%)."

    # 4. Fallback to presence check (pass) when population is null
    record_fallback_pass = deepcopy(VALID_BASE_RECORD)
    record_fallback_pass["impact"]["beneficiaries"]["beneficiaries"] = [
        {"location": "HK", "population": None, "beneficiary_type": "wild_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}},
        {"location": "HK", "population": None, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}},
    ]
    response = client.post("/audit", json=record_fallback_pass)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "pass"
    assert "Operates in high-neglectedness area(s): wild_animals. Population data not available" in item["details"]["calculation"]

    # 5. Fallback to presence check (warning) when population is null
    record_fallback_warning = deepcopy(VALID_BASE_RECORD)
    record_fallback_warning["impact"]["beneficiaries"]["beneficiaries"] = [
        {"location": "HK", "population": None, "beneficiary_type": "companion_animals", "source": {"source_type": "attached_report", "source_index": 0, "page_number": 1, "search_result_index": None, "quote": "...", "resolved_url": None}}
    ]
    response = client.post("/audit", json=record_fallback_warning)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "warning"
    assert "Operates in a low-neglectedness / saturated area (companion animals). Population data not available" in item["details"]["calculation"]

    # 6. Default status for missing impact data
    record_no_impact = deepcopy(VALID_BASE_RECORD)
    del record_no_impact["impact"]
    response = client.post("/audit", json=record_no_impact)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert "Impact data with beneficiary types is missing" in item["details"]["calculation"]