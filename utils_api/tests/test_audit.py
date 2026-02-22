from fastapi.testclient import TestClient

from app.schemas.organisation import OrganisationRecord


def test_run_audit_with_full_data(client: TestClient):
    from app.audits.registry import AUDIT_CHECKS
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
            "ratio_inputs": {
                "monthly_operating_expenses": 20000,
                "net_current_assets": 60000,
                "current_assets": 80000,
                "current_liabilities": 20000
            },
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
        },
        "impact": {
            "importance_factors": {
                "beneficiaries_demographic": [{
                    "location": "HK", "gender": "female", "age_range": "20-30",
                    "population": 100, "beneficiary_type": "human"
                }],
                "problem_profile": {
                    "problem_name": "Problem X", "target_population": "Group Y",
                    "severity_dimensions": [{
                        "dimension": "Health", "metric_name": "QALY",
                        "quantitative_data": {"value": 10, "unit": "years"},
                        "context_qualifier": "context", "counterfactual_baseline": {"description": "baseline", "value": 1},
                        "evidence_quality": "RCT/Meta-Analysis", "source_citation": "Source Z"
                    }]
                }
            },
            "tractability_factors": {"significant_events": [{"event_name": "E1", "summary": "S1"}], "evaluation_systems": "System A"},
            "neglectedness_factors": {"funding_sources": ["Gov"], "funding_landscape": "Crowded"}
        }
    }
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