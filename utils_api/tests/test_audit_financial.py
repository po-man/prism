from copy import deepcopy
from fastapi.testclient import TestClient

from app.schemas.organisation import OrganisationRecord
from tests.shared import VALID_BASE_RECORD


def get_audit_item(response_json: dict, item_id: str):
    """Helper to find a specific audit check item in the response."""
    return next((item for item in response_json["check_items"] if item["id"] == item_id), None)


def test_run_audit_with_liquidity_fallback(client: TestClient):
    """
    Tests that check_liquidity uses the fallback calculation when net_current_assets
    is missing but its component parts are present.
    """
    record_data = deepcopy(VALID_BASE_RECORD)
    # Explicitly set net_current_assets to None to test the fallback
    record_data["financials"]["ratio_inputs"]["net_current_assets"] = None

    OrganisationRecord.model_validate(record_data)

    response = client.post("/audit", json=record_data)
    assert response.status_code == 200
    result = response.json()

    liquidity_check = next((item for item in result["check_items"] if item["id"] == "check_liquidity"), None)
    assert liquidity_check is not None

    # The fallback should run. The result is (80000 - 20000) / 20000 = 3 months.
    # Per the new thresholds (>=3 & <6 mos), this is a 'warning'.
    assert liquidity_check["status"] == "warning"
    assert "($80,000 - $20,000)" in liquidity_check["details"]["calculation"]


def test_check_reserve_cap(client: TestClient):
    """Tests the check_reserve_cap audit for general reserves."""

    # 1. Pass for reserves <= 2 years
    record_pass = deepcopy(VALID_BASE_RECORD)
    record_pass["financials"]["reserves"]["total_reserves"] = 300000
    record_pass["financials"]["expenditure"]["total"] = 200000
    # Ratio = 1.5 years
    response = client.post("/audit", json=record_pass)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_reserve_cap")
    assert item["status"] == "pass"
    assert "1.5 years of expenditure" in item["details"]["calculation"]

    # 2. Warning for reserves > 2 and <= 5 years
    record_warn = deepcopy(VALID_BASE_RECORD)
    record_warn["financials"]["reserves"]["total_reserves"] = 500000
    record_warn["financials"]["expenditure"]["total"] = 200000
    # Ratio = 2.5 years
    response = client.post("/audit", json=record_warn)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_reserve_cap")
    assert item["status"] == "warning"
    assert "2.5 years of expenditure" in item["details"]["calculation"]

    # 3. Fail for reserves > 5 years
    record_fail = deepcopy(VALID_BASE_RECORD)
    record_fail["financials"]["reserves"]["total_reserves"] = 1200000
    record_fail["financials"]["expenditure"]["total"] = 200000
    # Ratio = 6.0 years
    response = client.post("/audit", json=record_fail)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_reserve_cap")
    assert item["status"] == "fail"
    assert "6.0 years of expenditure" in item["details"]["calculation"]

    # 4. Warning for zero or negative expenditure
    record_zero_exp = deepcopy(VALID_BASE_RECORD)
    record_zero_exp["financials"]["expenditure"]["total"] = 0
    response = client.post("/audit", json=record_zero_exp)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_reserve_cap")
    assert item["status"] == "warning"
    assert "is not a positive number, cannot compute ratio" in item["details"]["calculation"]

    # 5. Fail status for missing data
    record_missing = deepcopy(VALID_BASE_RECORD)
    record_missing["financials"]["reserves"]["total_reserves"] = None
    response = client.post("/audit", json=record_missing)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_reserve_cap")
    assert item["status"] == "fail"
    assert "Required financial data is missing" in item["details"]["calculation"]