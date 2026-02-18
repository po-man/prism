from fastapi.testclient import TestClient

from app.schemas.organisation import OrganisationRecord


def test_run_audit_with_full_data(client: TestClient):
    """
    Tests the /audit endpoint with a complete OrganisationRecord.
    It expects a successful response and checks the structure of the result.
    """
    # A sample record with all the necessary nested structures
    # This structure should align with the Pydantic models which are based on the JSON schemas.
    record_data = {
        "financials": {
            "financial_year": "2023-24",
            "income": {"donations": 500000, "government_grants": 250000, "total": 750000},
            "expenditure": {"administration": 100000, "fundraising": 50000, "program_services": 400000, "total": 550000},
            "lsg_specifics": {"lsg_reserve_amount": 50000, "provident_fund_reserve": 10000},
            "ratio_inputs": {"monthly_operating_expenses": 20000, "net_current_assets": 60000},
        },
        "governance": {
            "structure": {
                "board_size": 10,
                "board_members": [{"name": "John Doe", "title": "Chairman", "is_executive": False}],
                "committees": ["Audit", "Remuneration"]
            },
            "leadership": {"ceo_name": "Jane Doe", "ceo_title": "CEO"},
            "remuneration_disclosure": {
                "source_document_present": True,
                "top_tier_total_salary": 120000,
                "second_tier_total_salary": 90000,
                "third_tier_total_salary": 70000,
                "review_date": "2023-06-15"
            },
            "policies": {
                "has_conflict_of_interest": True,
                "has_whistleblowing": True,
                "has_investment_policy": True,
                "has_procurement_policy": True
            }
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