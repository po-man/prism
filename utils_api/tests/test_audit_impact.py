from copy import deepcopy
from fastapi.testclient import TestClient

# A valid base record to ensure requests pass Pydantic validation.
from tests.shared import VALID_BASE_RECORD


def get_audit_item(response_json: dict, item_id: str):
    """Helper to find a specific audit check item in the response."""
    return next((item for item in response_json["check_items"] if item["id"] == item_id), None)


def get_calculated_metric(response_json: dict, metric_id: str):
    """Helper to find a specific calculated metric in the response."""
    return next((metric for metric in response_json["calculated_metrics"] if metric["id"] == metric_id), None)


def test_check_evidence_quality(client: TestClient):
    """Tests the check_evidence_quality audit for various evidence levels."""
    # 1. Pass with high-quality evidence
    record_high_evidence = deepcopy(VALID_BASE_RECORD)
    record_high_evidence["impact"]["metrics"][0]["evidence_quality"] = "Quasi-Experimental"
    record_high_evidence["impact"]["metrics"][0]["evidence_quote"] = "We saw a 50% increase."
    response = client.post("/audit", json=record_high_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality")
    assert item["status"] == "pass"
    assert item["details"]["calculation"] == "Highest evidence found: 'Quasi-Experimental'."
    assert item["details"]["elaboration"] == "Quote: 'We saw a 50% increase.'"

    # 2. Warning with only low-quality evidence
    record_low_evidence = deepcopy(VALID_BASE_RECORD)
    record_low_evidence["impact"]["metrics"][0]["evidence_quality"] = "Pre-Post"
    record_low_evidence["impact"]["metrics"][0]["evidence_quote"] = None # Explicitly remove for this test
    record_low_evidence["impact"]["metrics"][0]["source_url"] = None

    response = client.post("/audit", json=record_low_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "Highest evidence found: 'Pre-Post'."
    assert item["details"]["elaboration"] is None # No quote in base record

    # 3. Warning when no evidence is specified
    record_no_evidence = deepcopy(VALID_BASE_RECORD)
    record_no_evidence["impact"]["metrics"] = []
    response = client.post("/audit", json=record_no_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality") # check_evidence_quality defaults to null status
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "No impact metrics were provided to assess evidence quality."

    # 4. Default status with missing impact data
    record_missing_impact = deepcopy(VALID_BASE_RECORD)
    del record_missing_impact["impact"]
    response = client.post("/audit", json=record_missing_impact)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality")
    assert item["details"]["calculation"] == "Impact data with metrics is missing."


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
    record_no_value["impact"]["metrics"][0]["counterfactual_baseline"]["value"] = None
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


def test_check_cost_per_outcome(client: TestClient):
    """Tests the calculate_cost_per_outcome metric, including edge cases."""

    # 1. Correct calculation with valid data (uses sum of beneficiaries)
    record_valid = deepcopy(VALID_BASE_RECORD)
    record_valid["financials"]["expenditure"]["program_services"] = 100000
    record_valid["impact"]["beneficiaries"] = [
        {"location": "HK", "population": 500, "beneficiary_type": "companion_animals"},
        {"location": "HK", "population": 1500, "beneficiary_type": "wild_animals"},
    ] # Total beneficiaries = 2000
    response = client.post("/audit", json=record_valid)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item is not None
    assert item["details"]["calculation"] == "($100,000 / 2,000 total beneficiaries) = $50.00 per outcome. | A $1,000 donation achieves ≈ 20 outcomes."

    # 2. Correct calculation with fallback to quant_data.value
    record_fallback = deepcopy(VALID_BASE_RECORD)
    record_fallback["financials"]["expenditure"]["program_services"] = 100000
    record_fallback["impact"]["beneficiaries"] = [{"location": "HK", "population": 0, "beneficiary_type": "companion_animals"}]
    record_fallback["impact"]["metrics"][0]["quantitative_data"]["value"] = 500 # Fallback value
    response = client.post("/audit", json=record_fallback)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item is not None
    assert item["details"]["calculation"] == "($100,000 / 500 total beneficiaries) = $200.00 per outcome. | A $1,000 donation achieves ≈ 5 outcomes."

    # 3. Handles missing financial data
    record_no_financials = deepcopy(VALID_BASE_RECORD)
    record_no_financials["financials"]["expenditure"]["program_services"] = None
    response = client.post("/audit", json=record_no_financials)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item is None # Function should return None

    # 4. Handles zero program spend
    record_zero_spend = deepcopy(VALID_BASE_RECORD)
    record_zero_spend["financials"]["expenditure"]["program_services"] = 0
    response = client.post("/audit", json=record_zero_spend)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item is not None
    assert item["details"]["calculation"] == "($0 / 500 total beneficiaries) = $0.00 per outcome" # No translation for $0 cost

    # 5. Handles zero primary outcome value
    record_zero_outcome = deepcopy(VALID_BASE_RECORD)
    # Set beneficiary population to 0 and metric value to 0 to test zero outcome.
    record_zero_outcome["impact"]["beneficiaries"][0]["population"] = 0
    record_zero_outcome["impact"]["metrics"][0]["quantitative_data"]["value"] = 0
    response = client.post("/audit", json=record_zero_outcome)
    assert response.status_code == 200
    item = get_calculated_metric(response.json(), "cost_per_outcome")
    assert item is None # Function should return None


def test_check_funding_neglectedness(client: TestClient):
    """Tests the check_funding_neglectedness audit."""

    # 1. Pass for medium neglectedness (between 40% and 80% inclusive)
    record_medium = deepcopy(VALID_BASE_RECORD)
    record_medium["financials"]["income"]["total"] = 1000000
    record_medium["financials"]["income"]["government_grants"] = 500000 # 50%
    response = client.post("/audit", json=record_medium)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["status"] == "pass"
    assert "50.0%" in item["details"]["calculation"]

    # 2. Pass for high neglectedness (< 40%)
    record_high = deepcopy(VALID_BASE_RECORD)
    record_high["financials"]["income"]["total"] = 1000000
    record_high["financials"]["income"]["government_grants"] = 200000 # 20%
    response = client.post("/audit", json=record_high)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["status"] == "pass"
    assert "20.0%" in item["details"]["calculation"]

    # 3. Fail for low neglectedness (> 80%)
    record_low = deepcopy(VALID_BASE_RECORD)
    record_low["financials"]["income"]["total"] = 1000000
    record_low["financials"]["income"]["government_grants"] = 850000 # 85%
    response = client.post("/audit", json=record_low)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["status"] == "fail"
    assert "85.0%" in item["details"]["calculation"]

    # 4. Handles zero total income
    record_zero_income = deepcopy(VALID_BASE_RECORD)
    record_zero_income["financials"]["income"]["total"] = 0
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
    record_pass["impact"]["beneficiaries"] = [
        {"location": "HK", "population": 800, "beneficiary_type": "wild_animals"},
        {"location": "HK", "population": 200, "beneficiary_type": "companion_animals"},
    ]
    response = client.post("/audit", json=record_pass)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "pass"
    assert item["details"]["calculation"] == "Focus on high-neglectedness areas (Wild Animals: 80%, Companion Animals: 20%)."

    # 2. Warning for < 50% high-neglectedness population
    record_warning_mixed = deepcopy(VALID_BASE_RECORD)
    record_warning_mixed["impact"]["beneficiaries"] = [
        {"location": "HK", "population": 150, "beneficiary_type": "farmed_animals"},
        {"location": "HK", "population": 850, "beneficiary_type": "companion_animals"},
    ]
    response = client.post("/audit", json=record_warning_mixed)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "Mixed portfolio with minority focus on high-neglectedness areas (Farmed Animals: 15%, Companion Animals: 85%)."

    # 3. Fail for 100% low-neglectedness population
    record_warning_low = deepcopy(VALID_BASE_RECORD)
    record_warning_low["impact"]["beneficiaries"] = [
        {"location": "HK", "population": 1000, "beneficiary_type": "companion_animals"}
    ]
    response = client.post("/audit", json=record_warning_low)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "fail"
    assert item["details"]["calculation"] == "Operates in a low-neglectedness / saturated area (Companion Animals: 100%)."

    # 4. Fallback to presence check (pass) when population is null
    record_fallback_pass = deepcopy(VALID_BASE_RECORD)
    record_fallback_pass["impact"]["beneficiaries"] = [
        {"location": "HK", "population": None, "beneficiary_type": "wild_animals"},
        {"location": "HK", "population": None, "beneficiary_type": "companion_animals"},
    ]
    response = client.post("/audit", json=record_fallback_pass)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cause_area_neglectedness")
    assert item["status"] == "pass"
    assert "Operates in high-neglectedness area(s): wild_animals. Population data not available" in item["details"]["calculation"]

    # 5. Fallback to presence check (warning) when population is null
    record_fallback_warning = deepcopy(VALID_BASE_RECORD)
    record_fallback_warning["impact"]["beneficiaries"] = [
        {"location": "HK", "population": None, "beneficiary_type": "companion_animals"}
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