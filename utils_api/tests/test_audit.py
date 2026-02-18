from fastapi.testclient import TestClient

from app.schemas.organisation import OrganisationRecord


def test_run_audit_with_full_data(client: TestClient):
    """
    Tests the /audit endpoint with a complete OrganisationRecord.
    It expects a successful response and checks the structure of the result.
    """
    # A sample record with all the necessary nested structures
    record_data = {
        "financials": {
            "lsg_reserve_amount": 50000,
            "operating_expenditure": 250000,
            "net_current_assets": 60000,
            "monthly_operating_expenses": 20000
        },
        "governance": {
            "rem_pkg_review_report": True
        }
    }
    # Validate with the Pydantic model before sending
    OrganisationRecord.model_validate(record_data)

    response = client.post("/audit", json=record_data)

    assert response.status_code == 200
    result = response.json()

    assert "analytics" in result
    assert isinstance(result["analytics"], list)
    assert len(result["analytics"]) == 3  # Based on current registry

    # Check for the IDs of the registered audit checks
    check_ids = {item["id"] for item in result["analytics"]}
    assert "check_reserve_cap" in check_ids
    assert "check_liquidity" in check_ids
    assert "check_remuneration" in check_ids


def test_run_audit_with_empty_data(client: TestClient):
    """
    Tests the /audit endpoint with an empty object.
    The endpoint should still run the checks, which will gracefully handle missing data.
    """
    response = client.post("/audit", json={})
    assert response.status_code == 200
    result = response.json()
    assert len(result["analytics"]) == 3