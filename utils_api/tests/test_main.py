import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def set_schema_dir():
    """
    Set the SCHEMA_DIR environment variable before any tests run.
    This fixture is autouse=True and session-scoped to ensure it runs once
    at the beginning of the test session, before any modules are imported by fixtures.
    """
    # The project root for utils_api is the parent of the 'tests' directory
    utils_api_root = Path(__file__).parent.parent
    os.environ["SCHEMA_DIR"] = str(utils_api_root.parent / "schemas")


@pytest.fixture(scope="module")
def client():
    """A TestClient fixture that imports the app after the environment is set."""
    from app.main import app  # Import here to ensure SCHEMA_DIR is set
    with TestClient(app) as c:
        yield c

# --- Test Data ---

VALID_FINANCIALS = {
    "financial_year": "2023-24",
    "income": {"donations": 100, "government_grants": 200, "total": 300},
    "expenditure": {"administration": 50, "fundraising": 20, "program_services": 150, "total": 220},
    "lsg_specifics": {"lsg_reserve_amount": 10, "provident_fund_reserve": 5},
    "ratio_inputs": {"monthly_operating_expenses": 18, "net_current_assets": 40},
}

VALID_IMPACT = {
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
                    "context_qualifier": "context", "counterfactual_baseline": {"description": "baseline"},
                    "evidence_quality": "High", "source_citation": "Source Z"
                }]
            }
        },
        "tractability_factors": {"significant_events": [{"event_name": "E1", "summary": "S1"}], "evaluation_systems": "System A"},
        "neglectedness_factors": {"funding_sources": ["Gov"], "funding_landscape": "Crowded"}
    }
}

VALID_GOVERNANCE = {
    "governance": {
        "structure": {
            "board_size": 10,
            "board_members": [{"name": "John Doe", "title": "Chairman", "is_executive": False}],
            "committees": ["Audit"]
        },
        "leadership": {"ceo_name": "Jane Doe", "ceo_title": "CEO"},
        "remuneration_disclosure": {
            "source_document_present": True, "top_tier_total_salary": 100000,
            "second_tier_total_salary": 80000, "third_tier_total_salary": 60000,
            "review_date": "2023-01-01"
        },
        "policies": {
            "has_conflict_of_interest": True, "has_whistleblowing": True,
            "has_investment_policy": True, "has_procurement_policy": False
        }
    }
}

VALID_RISK = {
    "analysis_date": "2023-01-01",
    "overall_risk_level": "LOW",
    "risk_dimensions": {
        "reputational": {"flagged": False, "severity": None, "summary": "None"},
        "governance_executive": {"flagged": False, "summary": "None"},
        "regulatory": {"flagged": False, "summary": "None"}
    },
    "key_incidents": [{"year": 2022, "description": "Incident A", "source_url": "http://a.com", "reliability": "HIGH"}]
}


@pytest.mark.parametrize("schema_name, valid_data", [
    ("v1/financials.schema.json", VALID_FINANCIALS),
    ("v1/impact.schema.json", VALID_IMPACT),
    ("v1/governance.schema.json", VALID_GOVERNANCE),
    ("v1/risk.schema.json", VALID_RISK),
])
def test_validate_valid_data(client, schema_name, valid_data):
    """Tests that valid data passes validation for each schema."""
    response = client.post("/validate", json={"schema_name": schema_name, "data": valid_data})
    assert response.status_code == 200
    result = response.json()
    assert result["valid"] is True
    assert "details" not in result


@pytest.mark.parametrize("schema_name, invalid_data, expected_error_part", [
    # Financials: missing required top-level field
    ("v1/financials.schema.json", {
        k: v for k, v in VALID_FINANCIALS.items()
        if k != "income"
    }, "'income' is a required property"),
    # Impact: wrong type for a nested field
    ("v1/impact.schema.json", {
        "impact": {
            **VALID_IMPACT["impact"],
            "importance_factors": {
                **VALID_IMPACT["impact"]["importance_factors"],
                "beneficiaries_demographic": "not-an-array"
            }
        }
    }, "is not of type 'array'"),
    # Governance: missing a required field in a nested object
    ("v1/governance.schema.json", {
        **VALID_GOVERNANCE,
        "governance": {
            **VALID_GOVERNANCE["governance"],
            "structure": {
                k: v for k, v in VALID_GOVERNANCE["governance"]["structure"].items()
                if k != "board_members"
            }
        }
    }, "'board_members' is a required property"),
    # Risk: wrong enum value
    ("v1/risk.schema.json", {**VALID_RISK, "overall_risk_level": "UNKNOWN"}, "is not one of ['LOW', 'MEDIUM', 'HIGH']"),
])
def test_validate_invalid_data(client, schema_name, invalid_data, expected_error_part):
    """Tests that invalid data fails validation with a descriptive error."""
    response = client.post("/validate", json={"schema_name": schema_name, "data": invalid_data})
    assert response.status_code == 200
    result = response.json()
    assert result["valid"] is False
    assert "details" in result
    print("message")
    print(result["details"]["message"])
    assert expected_error_part in result["details"]["message"]


def test_validate_non_existent_schema(client):
    """Tests that a request for a non-existent schema returns a 404 error."""
    response = client.post("/validate", json={"schema_name": "v1/non_existent.schema.json", "data": {}})
    assert response.status_code == 404
    result = response.json()
    assert "Schema 'v1/non_existent.schema.json' not found" in result["detail"]


def test_validate_bad_request_body_missing_schema_name(client):
    """Tests that a request missing 'schema_name' is rejected."""
    response = client.post("/validate", json={"data": {}})
    assert response.status_code == 422  # Unprocessable Entity


def test_validate_bad_request_body_missing_data(client):
    """Tests that a request missing 'data' is rejected."""
    response = client.post("/validate", json={"schema_name": "v1/financials.schema.json"})
    assert response.status_code == 422  # Unprocessable Entity
