import pytest
from fastapi.testclient import TestClient


# --- Test Data ---

VALID_FINANCIALS = {
    "financial_year": "2023-24",
    "currency": {
        "original_code": "HKD",
        "usd_exchange_rate": 0.128,
        "rate_date": "2023-12-31",
    },
    "income": {
        "donations": {"value": 100},
        "government_grants": {"value": 200},
        "total": {"value": 300}
    },
    "expenditure": {
        "administration": {"value": 50},
        "fundraising": {"value": 20},
        "program_services": {"value": 150},
        "total": {"value": 220}
    },
    "reserves": {"total_reserves": {"value": 75000}},
    "lsg_specifics": {
        "lsg_reserve_amount": {"value": 10},
        "provident_fund_reserve": {"value": 5}
    },
    "ratio_inputs": {
        "monthly_operating_expenses": {"value": 18},
        "net_current_assets": {"value": 40},
        "current_assets": {"value": 50},
        "current_liabilities": {"value": 10}
    }
}

VALID_IMPACT = {
    "beneficiaries": [{
        "location": "Hong Kong",
        "population": 500,
        "beneficiary_type": "companion_animals",
        "source": {
            "source_type": "attached_report",
            "source_index": 0,
            "page_number": 15,
            "search_result_index": None,
            "quote": "We provided services to 500 companion animals.",
            "resolved_url": None
        }
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
        "timeframe": "annual",
        "source": {
            "source_type": "attached_report",
            "source_index": 0,
            "page_number": 12,
            "search_result_index": None,
            "quote": "The study showed a significant increase in animal welfare.",
            "resolved_url": None
        }
    }],
    "significant_events": [{
        "event_name": "Project Shelter",
        "summary": "Built a new shelter facility.",
        "intervention_type": ["individual_rescue_and_sanctuary"],
        "intervention_type_other_description": None,
        "timeframe": "annual",
        "source": {
            "source_type": "web_search",
            "source_index": None,
            "page_number": None,
            "search_result_index": 0,
            "quote": "Our new shelter facility, 'Project Shelter', opened this year.",
            "resolved_url": None
        }
    }],
    "context": {
        "operating_scope": "pure_animal_advocacy",
        "explicit_unit_cost": {
            "amount": 100,
            "currency": "HKD",
            "description": "Cost to spay one dog."
        },
    }
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
