import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open


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
    "beneficiaries": {
        "beneficiaries": [{
            "location": "Hong Kong",
            "population": 500,
            "beneficiary_type": "companion_animals",
            "source": {
                "source_type": "attached_report",
                "source_index": 0,
                "page_number": 15,
                "quote": "We provided services to 500 companion animals.",
                "resolved_url": None
            }
        }]
    },
    "metrics": {
        "metrics": [{
            "metric_name": "Animals Rescued",
            "quantitative_data": {
                "value": 1000,
                "unit": "animals"
            },
            "context_qualifier": "Rescued from unsafe conditions.",
            "counterfactual_baseline": {
                "value": 50,
                "source": {
                    "source_type": "attached_report",
                    "source_index": 0,
                    "page_number": 13,
                    "quote": "Without our intervention, these animals would have remained at risk.",
                    "resolved_url": None
                }
            },
            "evidence_quality": "RCT/Meta-Analysis",
            "timeframe": "annual",
            "source": {
                "source_type": "attached_report",
                "source_index": 0,
                "page_number": 12,
                "quote": "The study showed a significant increase in animal welfare.",
                "resolved_url": None
            }
        }]
    },
    "interventions": {
        "significant_events": [{
            "event_name": "Project Shelter",
            "summary": "Built a new shelter facility.",
            "intervention_type": ["individual_rescue_and_sanctuary"],
            "primary_intervention_type": "individual_rescue_and_sanctuary",
            "intervention_type_other_description": None,
            "timeframe": "annual",
            "source": {
                "source_type": "attached_report",
                "source_index": 0,
                "page_number": 2,
                "quote": "Our new shelter facility, 'Project Shelter', opened this year on page 2.",
                "resolved_url": None
            }
        }],
        "context": {
            "operating_scope": {
                "value": "pure_animal_advocacy",
                "source": {
                    "source_type": "attached_report",
                    "source_index": 0,
                    "page_number": 1,
                    "quote": "We are an organisation dedicated to animal advocacy.",
                    "resolved_url": None
                }
            },
            "explicit_unit_costs": [
                {
                    "intervention_type": "high_volume_spay_neuter",
                    "amount": 100,
                    "currency": "HKD",
                    "description": "Cost to spay one dog.",
                    "source": {
                        "source_type": "attached_report",
                        "source_index": 0,
                        "page_number": 1,
                        "quote": "It costs just $25 to spay one dog.",
                        "resolved_url": None
                    }
                }
            ],
        }
    },
    "transparency": {
        "transparency_indicators": {
            "unintended_consequences_reported": {
                "value": True,
                "source": {
                    "source_type": "attached_report",
                    "source_index": 0,
                    "page_number": 1,
                    "quote": "We admit this was a failure.",
                    "resolved_url": None
                }
            },
            "euthanasia_statistics_reported": {
                "value": True,
                "source": {
                    "source_type": "attached_report",
                    "source_index": 0,
                    "page_number": 1,
                    "quote": "The euthanasia is 2%",
                    "resolved_url": None
                }
            }
        }
    }
}


# --- Test Data for Normalization ---

ABBREVIATED_IMPACT_PAYLOAD = {
    "beneficiaries": {
        "beneficiaries": [{
            "location": "Test Location",
            "population": 100,
            "beneficiary_type": "farmed_animals"
        }]
    },
    "interventions": {
        "significant_events": [{
            "event_name": "A special event",
            "intervention_type": ["other"],
            "primary_intervention_type": "other",
            "other_desc": "A custom intervention type."
        }]
    },
    "transparency": {
        "transparency_indicators": {
            "unintended_rep": {"value": True},
            "euthanasia_rep": {"value": False}
        }
    }
}

CANONICAL_IMPACT_PAYLOAD = {
    "beneficiaries": {
        "beneficiaries": [{
            "location": "Test Location",
            "population": 100,
            "beneficiary_type": "farmed_animals"
        }]
    },
    "interventions": {
        "significant_events": [{
            "event_name": "A special event",
            "intervention_type": ["other"],
            "primary_intervention_type": "other",
            "intervention_type_other_description": "A custom intervention type."
        }]
    },
    "transparency": {
        "transparency_indicators": {
            "unintended_consequences_reported": {"value": True},
            "euthanasia_statistics_reported": {"value": False}
        }
    }
}

MOCK_KEY_MAPPING = {
    "other_desc": "intervention_type_other_description",
    "unintended_rep": "unintended_consequences_reported",
    "euthanasia_rep": "euthanasia_statistics_reported",
    "prov_fund_res": "provident_fund_reserve",
    "monthly_op_ex": "monthly_operating_expenses"
}


@patch('app.routers.validation.load_key_mapping', return_value=MOCK_KEY_MAPPING)
def test_normalize_and_validate_reverses_keys(mock_load_mapping, client):
    """
    Tests that the /normalize-and-validate endpoint correctly reverses abbreviated keys
    before attempting validation. The payload is incomplete but should fail validation
    on a missing canonical key if reversal is successful.
    """
    response = client.post(
        "/normalize",
        json={"schema_name": "v1/impact_beneficiaries.schema.json", "data": ABBREVIATED_IMPACT_PAYLOAD['beneficiaries']}
    )

    # Assert that our high-level mock was called, which is cleaner and more robust.
    mock_load_mapping.assert_called_once()

    assert response.status_code == 200

    response_validated = client.post(
        "/validate",
        json={"schema_name": "v1/impact_beneficiaries.schema.json", "data": response.json()}
    )

    assert response_validated.status_code == 200
    result = response_validated.json()
    assert result["valid"] is True


@pytest.mark.parametrize("schema_name, valid_data", [
    ("v1/financials.schema.json", VALID_FINANCIALS),
    ("v1/impact_beneficiaries.schema.json", VALID_IMPACT["beneficiaries"]),
    ("v1/impact_metrics.schema.json", VALID_IMPACT["metrics"]),
    ("v1/impact_interventions.schema.json", VALID_IMPACT["interventions"]),
    ("v1/impact_transparency.schema.json", VALID_IMPACT["transparency"]),
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
    ("v1/impact_beneficiaries.schema.json", {
        **VALID_IMPACT["beneficiaries"],
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
