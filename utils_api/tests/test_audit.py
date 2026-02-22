from fastapi.testclient import TestClient

from app.schemas.organisation import OrganisationRecord
from tests.shared import VALID_BASE_RECORD


def test_run_audit_with_full_data(client: TestClient):
    from app.audits.registry import AUDIT_CHECKS
    """
    Tests the /audit endpoint with a complete OrganisationRecord.
    It expects a successful response and checks the structure of the result.
    """
    record_data = VALID_BASE_RECORD
    # Validate with the Pydantic model before sending
    OrganisationRecord.model_validate(record_data)

    response = client.post("/audit", json=record_data)

    assert response.status_code == 200
    result = response.json()

    assert "check_items" in result
    assert isinstance(result["check_items"], list)
    assert len(result["check_items"]) == len(AUDIT_CHECKS)  # Based on current registry

    # Check for the IDs of the registered audit checks
    check_ids = {item["id"] for item in result["check_items"]}
    expected_ids = {check.__name__ for check in AUDIT_CHECKS}
    assert check_ids == expected_ids


def test_run_audit_with_empty_data(client: TestClient):
    from app.audits.registry import AUDIT_CHECKS
    """
    Tests the /audit endpoint with an empty object.
    The endpoint should still run the checks, which will gracefully handle missing data.
    """
    response = client.post("/audit", json={})
    assert response.status_code == 200
    result = response.json()
    assert "check_items" in result
    assert isinstance(result["check_items"], list)
    assert len(result["check_items"]) == len(AUDIT_CHECKS)