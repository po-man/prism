from copy import deepcopy

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def base_payload():
    """Provides a base payload with various source types to be resolved."""
    return {
        "data": [
            {
                "id": "item1",
                "source": {
                    "source_type": "attached_report",
                    "source_index": 0,
                    "page_number": 12,
                    "quote": "This is from the annual report.",
                    "resolved_url": None,
                },
            },
            {
                "id": "item2",
                "nested_data": {"source": None},
            },
            {
                "id": "item3",
                "source": {
                    "source_type": "attached_report",
                    "source_index": 1,
                    "page_number": 3,
                    "quote": "This is from the financial report.",
                    "resolved_url": None,
                },
            },
            {
                "id": "item4_no_change",
                "source": None,
            },
        ],
        "context": {
            "attached_reports": [
                "https://example.com/annual_report.pdf",
                "https://example.com/financial_report.pdf",
            ],
        },
    }


def test_resolve_provenance_success(client: TestClient, base_payload: dict):
    """
    Tests that the /resolve-provenance endpoint correctly populates the
    `resolved_url` for 'attached_report' source types.
    """
    response = client.post("/resolve-provenance", json=base_payload)
    assert response.status_code == 200
    result = response.json()["data"]

    # Test attached_report resolution
    assert (
        result[0]["source"]["resolved_url"]
        == "https://example.com/annual_report.pdf#page=12"
    )
    assert (
        result[2]["source"]["resolved_url"]
        == "https://example.com/financial_report.pdf#page=3"
    )


def test_resolve_provenance_no_sources(client: TestClient, base_payload: dict):
    """
    Tests that the endpoint runs without error and makes no changes when the
    data contains no 'source' objects to resolve.
    """
    payload = deepcopy(base_payload)
    # Remove all source objects
    del payload["data"][0]["source"]
    del payload["data"][2]["source"]

    response = client.post("/resolve-provenance", json=payload)
    assert response.status_code == 200
    assert response.json()["data"] == payload["data"]