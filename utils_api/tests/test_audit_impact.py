from copy import deepcopy
from fastapi.testclient import TestClient

# A valid base record to ensure requests pass Pydantic validation.
# We will modify this for each test case.
VALID_BASE_RECORD = {
    "financials": {
        "financial_year": "2023-24",
        "income": {"donations": 500000, "government_grants": 250000, "total": 750000},
        "expenditure": {"administration": 100000, "fundraising": 50000, "program_services": 400000, "total": 550000},
        "lsg_specifics": {"lsg_reserve_amount": 50000, "provident_fund_reserve": 10000},
        "ratio_inputs": {"monthly_operating_expenses": 20000, "net_current_assets": 60000, "current_assets": 80000, "current_liabilities": 20000},
    },
    "impact": {
        "importance_factors": {
            "beneficiaries_demographic": [{"location": "HK", "gender": "female", "age_range": "20-30", "population": 500, "beneficiary_type": "human"}],
            "problem_profile": {
                "problem_name": "Problem X", "target_population": "Group Y",
                "severity_dimensions": [{
                    "dimension": "Health", "metric_name": "QALY", "quantitative_data": {"value": 1000, "unit": "years"},
                    "context_qualifier": "context", "counterfactual_baseline": {"description": "baseline", "value": 1},
                    "evidence_quality": "RCT/Meta-Analysis", "source_citation": "Source Z"
                }]
            }
        },
        "tractability_factors": {"significant_events": [{"event_name": "E1", "summary": "S1"}], "evaluation_systems": "System A"},
        "neglectedness_factors": {"funding_sources": ["Gov"], "funding_landscape": "Crowded"}
    }
}


def get_audit_item(response_json: dict, item_id: str):
    """Helper to find a specific audit check item in the response."""
    return next((item for item in response_json["check_items"] if item["id"] == item_id), None)


def test_check_evidence_quality(client: TestClient):
    """Tests the check_evidence_quality audit for various evidence levels."""
    # 1. Pass with high-quality evidence
    record_high_evidence = deepcopy(VALID_BASE_RECORD)
    record_high_evidence["impact"]["importance_factors"]["problem_profile"]["severity_dimensions"].append(
        {"evidence_quality": "Quasi-Experimental", "dimension": "Health", "metric_name": "DALY", "quantitative_data": {"value": 5, "unit": "years"}, "context_qualifier": "context", "counterfactual_baseline": {"description": "baseline", "value": 1}, "source_citation": "Source Y"}
    )
    response = client.post("/audit", json=record_high_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality")
    assert item["status"] == "pass"
    assert item["details"]["calculation"] == "Highest evidence found: 'RCT/Meta-Analysis'."

    # 2. Warning with only low-quality evidence
    record_low_evidence = deepcopy(VALID_BASE_RECORD)
    record_low_evidence["impact"]["importance_factors"]["problem_profile"]["severity_dimensions"][0]["evidence_quality"] = "Pre-Post"

    response = client.post("/audit", json=record_low_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "Highest evidence found: 'Pre-Post'."

    # 3. Warning when no evidence is specified
    record_no_evidence = deepcopy(VALID_BASE_RECORD)
    record_no_evidence["impact"]["importance_factors"]["problem_profile"]["severity_dimensions"] = []
    response = client.post("/audit", json=record_no_evidence)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality")
    assert item["status"] == "warning"
    assert item["details"]["calculation"] == "No evidence quality was specified in any impact claim."

    # 4. Null status with missing impact data
    record_missing_impact = deepcopy(VALID_BASE_RECORD)
    del record_missing_impact["impact"]
    response = client.post("/audit", json=record_missing_impact)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_evidence_quality")
    assert item["details"]["calculation"] == "Impact data with severity dimensions is missing."


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
    record_no_value["impact"]["importance_factors"]["problem_profile"]["severity_dimensions"][0][
        "counterfactual_baseline"
    ]["value"] = None
    response = client.post("/audit", json=record_no_value)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_counterfactual_baseline")
    assert item["status"] == "fail"
    assert item["details"]["calculation"] == "No quantified counterfactual baseline was provided."

    # 4. Null status with missing impact data
    record_missing_impact = deepcopy(VALID_BASE_RECORD)
    del record_missing_impact["impact"]
    response = client.post("/audit", json=record_missing_impact)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_counterfactual_baseline")
    assert item["details"]["calculation"] == "Impact data with severity dimensions is missing."


def test_check_cost_per_outcome(client: TestClient):
    """Tests the check_cost_per_outcome audit, including edge cases."""

    # 1. Correct calculation with valid data (primary outcome is quant_data.value)
    record_valid = deepcopy(VALID_BASE_RECORD)
    record_valid["financials"]["expenditure"]["program_services"] = 100000
    # Base record has quant_data.value=1000 and population=500, so max is 1000
    response = client.post("/audit", json=record_valid)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cost_per_outcome")
    assert item["status"] == "null"  # Informational check
    assert item["details"]["calculation"] == "($100,000 / 1,000 beneficiaries) = $100.00 per outcome"

    # 2. Handles missing financial data
    record_no_financials = deepcopy(VALID_BASE_RECORD)
    record_no_financials["financials"]["expenditure"]["program_services"] = None
    response = client.post("/audit", json=record_no_financials)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cost_per_outcome")
    assert item["details"]["calculation"] == "Financials with program services expenditure are missing."

    # 3. Handles zero program spend
    record_zero_spend = deepcopy(VALID_BASE_RECORD)
    record_zero_spend["financials"]["expenditure"]["program_services"] = 0
    response = client.post("/audit", json=record_zero_spend)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cost_per_outcome")
    assert item["details"]["calculation"] == "($0 / 1,000 beneficiaries) = $0.00 per outcome"

    # 4. Handles zero primary outcome value
    record_zero_outcome = deepcopy(VALID_BASE_RECORD)
    # Set one outcome to 0 and another to a negative value, so the max() is 0.
    record_zero_outcome["impact"]["importance_factors"]["beneficiaries_demographic"][0]["population"] = 0
    record_zero_outcome["impact"]["importance_factors"]["problem_profile"]["severity_dimensions"][0]["quantitative_data"]["value"] = -1
    response = client.post("/audit", json=record_zero_outcome)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_cost_per_outcome")
    assert item["details"]["calculation"] == "Primary outcome value (0) is not a positive number."


def test_check_funding_neglectedness(client: TestClient):
    """Tests the check_funding_neglectedness audit."""

    # 1. Pass for medium neglectedness (between 40% and 80%)
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

    # 3. Warning for low neglectedness (> 80%)
    record_low = deepcopy(VALID_BASE_RECORD)
    record_low["financials"]["income"]["total"] = 1000000
    record_low["financials"]["income"]["government_grants"] = 850000 # 85%
    response = client.post("/audit", json=record_low)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["status"] == "warning"
    assert "85.0%" in item["details"]["calculation"]

    # 4. Handles zero total income
    record_zero_income = deepcopy(VALID_BASE_RECORD)
    record_zero_income["financials"]["income"]["total"] = 0
    response = client.post("/audit", json=record_zero_income)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert "is not a positive number" in item["details"]["calculation"]

    # 5. Null status for missing financial data
    record_missing_financials = deepcopy(VALID_BASE_RECORD)
    del record_missing_financials["financials"]
    response = client.post("/audit", json=record_missing_financials)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_funding_neglectedness")
    assert item["details"]["calculation"] == "Financials with income breakdown are missing."