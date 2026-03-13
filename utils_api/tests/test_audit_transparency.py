from copy import deepcopy
from fastapi.testclient import TestClient

from tests.shared import VALID_BASE_RECORD


def get_audit_item(response_json: dict, item_id: str):
    """Helper to find a specific audit check item in the response."""
    return next((item for item in response_json["check_items"] if item["id"] == item_id), None)


def test_check_negative_impact_disclosure(client: TestClient):
    """
    Tests the check_negative_impact_disclosure audit.
    - Should return 'bonus' if disclosure is True.
    - Should return 'not_disclosed' if disclosure is False or data is missing.
    """
    # 1. Bonus: Disclosure is True
    record_bonus = deepcopy(VALID_BASE_RECORD)
    record_bonus["impact"]["transparency_indicators"]["unintended_consequences_reported"]["value"] = True
    response = client.post("/audit", json=record_bonus)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_negative_impact_disclosure")
    assert item is not None
    assert item["status"] == "bonus"
    assert "self-reported on unintended negative impacts" in item["details"]["calculation"]

    # 2. Not Disclosed: Disclosure is False
    record_not_disclosed = deepcopy(VALID_BASE_RECORD)
    record_not_disclosed["impact"]["transparency_indicators"]["unintended_consequences_reported"]["value"] = False
    response = client.post("/audit", json=record_not_disclosed)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_negative_impact_disclosure")
    assert item is not None
    assert item["status"] == "not_disclosed"
    assert "No disclosure of unintended negative impacts found" in item["details"]["calculation"]

    # 3. Not Disclosed: Data is missing
    record_missing = deepcopy(VALID_BASE_RECORD)
    del record_missing["impact"]["transparency_indicators"]["unintended_consequences_reported"]
    response = client.post("/audit", json=record_missing)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_negative_impact_disclosure")
    assert item is not None
    assert item["status"] == "not_disclosed"


def test_check_live_release_transparency(client: TestClient):
    """
    Tests the conditional logic of the check_live_release_transparency audit.
    - Should return 'n_a' if the org is not a direct shelter.
    - Should return 'bonus' if it is a shelter and discloses stats.
    - Should return 'not_disclosed' if it is a shelter and does not disclose.
    """
    # 1. N/A: Org does not engage in applicable interventions
    record_na = deepcopy(VALID_BASE_RECORD)
    record_na["impact"]["significant_events"][0]["intervention_type"] = ["corporate_welfare_campaigns"]
    response = client.post("/audit", json=record_na)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_live_release_transparency")
    assert item is not None
    assert item["status"] == "n_a"
    assert "does not engage in direct animal sheltering" in item["details"]["calculation"]

    # 2. Bonus: Applicable org discloses euthanasia stats
    record_bonus = deepcopy(VALID_BASE_RECORD)
    # Base record already has 'individual_rescue_and_sanctuary' and disclosure set to True
    response = client.post("/audit", json=record_bonus)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_live_release_transparency")
    assert item is not None
    assert item["status"] == "bonus"
    assert "provided euthanasia or live-release statistics" in item["details"]["calculation"]

    # 3. Not Disclosed: Applicable org does NOT disclose euthanasia stats
    record_not_disclosed = deepcopy(VALID_BASE_RECORD)
    record_not_disclosed["impact"]["transparency_indicators"]["euthanasia_statistics_reported"]["value"] = False
    response = client.post("/audit", json=record_not_disclosed)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_live_release_transparency")
    assert item is not None
    assert item["status"] == "not_disclosed"
    assert "No disclosure of euthanasia or live-release rates found" in item["details"]["calculation"]

    # 4. Bonus: Applicable via 'veterinary_care_and_treatment'
    record_bonus_vet = deepcopy(VALID_BASE_RECORD)
    record_bonus_vet["impact"]["significant_events"][0]["intervention_type"] = ["veterinary_care_and_treatment"]
    record_bonus_vet["impact"]["transparency_indicators"]["euthanasia_statistics_reported"]["value"] = True
    response = client.post("/audit", json=record_bonus_vet)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_live_release_transparency")
    assert item is not None
    assert item["status"] == "bonus"

    # 5. N/A: No significant events at all
    record_no_events = deepcopy(VALID_BASE_RECORD)
    record_no_events["impact"]["significant_events"] = []
    response = client.post("/audit", json=record_no_events)
    assert response.status_code == 200
    item = get_audit_item(response.json(), "check_live_release_transparency")
    assert item is not None
    assert item["status"] == "n_a"