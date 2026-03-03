import pytest
from fastapi.testclient import TestClient


# --- Test Data ---

VALID_FINANCIALS = {
    "financial_year": "2023-24",
    "income": {"donations": 100, "government_grants": 200, "total": 300},
    "expenditure": {"administration": 50, "fundraising": 20, "program_services": 150, "total": 220},
    "reserves": {"total_reserves": 75000},
    "lsg_specifics": {"lsg_reserve_amount": 10, "provident_fund_reserve": 5},
    "ratio_inputs": {
        "monthly_operating_expenses": 18,
        "net_current_assets": 40,
        "current_assets": 50,
        "current_liabilities": 10
    },
}

VALID_IMPACT = {
    "beneficiaries": [{
        "location": "Hong Kong",
        "population": 500,
        "beneficiary_type": "companion_animals"
    }],
    "metrics": [{
        "metric_name": "Animals Rescued",
        "quantitative_data": {
            "value": 1000,
            "unit": "animals"
        },
        "context_qualifier": "Rescued from unsafe conditions.",
        "counterfactual_baseline": {
            "description": "Without intervention, these animals would have remained at risk.",
            "value": 50
        },
        "evidence_quality": "RCT/Meta-Analysis",
        "source_citation": "Annual Report 2023, p. 12",
        "source_url": None,
        "evidence_quote": "The study showed a significant increase in animal welfare."
    }],
    "significant_events": [{
        "event_name": "Project Shelter",
        "summary": "Built a new shelter facility.",
        "intervention_type": "direct_care",
        "source_url": None,
        "source_quote": None
    }]
}


@pytest.mark.parametrize("schema_name, valid_data", [
    ("v1/financials.schema.json", VALID_FINANCIALS),
    ("v1/impact.schema.json", VALID_IMPACT),
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
        **VALID_IMPACT,
        "beneficiaries": "not-an-array"
    }, "is not of type 'array'"),
])
def test_validate_invalid_data(client, schema_name, invalid_data, expected_error_part):
    """Tests that invalid data fails validation with a descriptive error."""
    response = client.post("/validate", json={"schema_name": schema_name, "data": invalid_data})
    assert response.status_code == 200
    result = response.json()
    assert result["valid"] is False
    assert "details" in result
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
