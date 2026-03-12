from copy import deepcopy
from urllib.parse import quote as url_quote

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
                    "search_result_index": None,
                    "quote": "This is from the annual report.",
                    "resolved_url": None,
                },
            },
            {
                "id": "item2",
                "nested_data": {
                    "source": {
                        "source_type": "web_search",
                        "source_index": None,
                        "page_number": None,
                        "search_result_index": 1,
                        "quote": "A quote with special chars: &?#",
                        "resolved_url": None,
                    }
                },
            },
            {
                "id": "item3",
                "source": {
                    "source_type": "attached_report",
                    "source_index": 1,
                    "page_number": 3,
                    "search_result_index": None,
                    "quote": "This is from the financial report.",
                    "resolved_url": None,
                },
            },
            {
                "id": "item4_no_change",
                "source": {
                    "source_type": "web_search",
                    "search_result_index": 99,  # Index not in context
                    "quote": "This should not be resolved.",
                    "resolved_url": None,
                },
            },
        ],
        "context": {
            "attached_reports": [
                "https://example.com/annual_report.pdf",
                "https://example.com/financial_report.pdf",
            ],
            "web_search_results": [
                {"original_text": "...", "url": "https://example.org/news/1"},
                {"original_text": "...", "url": "https://example.org/blog/post-abc"},
            ],
        },
    }


def test_resolve_provenance_success(client: TestClient, base_payload: dict):
    """
    Tests that the /resolve-provenance endpoint correctly populates the
    `resolved_url` for both 'attached_report' and 'web_search' source types.
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

    # Test web_search resolution with URL encoding
    quote = "A quote with special chars: &?#"
    encoded_quote = url_quote(quote)
    expected_web_url = f"https://example.org/blog/post-abc#:~:text={encoded_quote}"
    assert result[1]["nested_data"]["source"]["resolved_url"] == expected_web_url

    # Test that a source with missing context remains unresolved
    assert result[3]["source"]["resolved_url"] is None


def test_resolve_provenance_no_sources(client: TestClient, base_payload: dict):
    """
    Tests that the endpoint runs without error and makes no changes when the
    data contains no 'source' objects to resolve.
    """
    payload = deepcopy(base_payload)
    # Remove all source objects
    del payload["data"][0]["source"]
    del payload["data"][1]["nested_data"]["source"]
    del payload["data"][2]["source"]
    del payload["data"][3]["source"]

    response = client.post("/resolve-provenance", json=payload)
    assert response.status_code == 200
    assert response.json()["data"] == payload["data"]