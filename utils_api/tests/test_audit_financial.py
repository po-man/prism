from copy import deepcopy
from fastapi.testclient import TestClient

from app.schemas.organisation import OrganisationRecord
from tests.shared import VALID_BASE_RECORD


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

    # The status should not be 'null' (Data Missing) because the fallback should have run.
    # It should be 'pass' because (80000 - 20000) / 20000 = 3, which is >= 3 months.
    assert liquidity_check["status"] == "pass"
    assert "($80,000 - $20,000)" in liquidity_check["details"]["calculation"]