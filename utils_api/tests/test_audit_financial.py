from fastapi.testclient import TestClient

from app.schemas.organisation import OrganisationRecord


def test_run_audit_with_liquidity_fallback(client: TestClient):
    """
    Tests that check_liquidity uses the fallback calculation when net_current_assets
    is missing but its component parts are present.
    """
    record_data = {
        "financials": {
            "financial_year": "2023-24",
            "income": {"donations": 500000, "government_grants": 250000, "total": 750000},
            "expenditure": {"administration": 100000, "fundraising": 50000, "program_services": 400000, "total": 550000},
            "lsg_specifics": {"lsg_reserve_amount": 50000, "provident_fund_reserve": 10000},
            "ratio_inputs": {
                "monthly_operating_expenses": 20000,
                "net_current_assets": None,  # Explicitly missing
                "current_assets": 80000,
                "current_liabilities": 20000
            },
        }
    }
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