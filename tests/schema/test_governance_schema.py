import json
from pathlib import Path
from typing import Any, Dict, List

import jsonschema
import pytest

# --- Test Configuration ---

PROJECT_ROOT = Path(__file__).parent.parent.parent

# List of tuples: (path_to_mock_file, expected_to_be_valid)
MOCK_FILES_TO_TEST = [
    (PROJECT_ROOT / "data/mocks/schemas/pass_full_compliance.json", True),
    (PROJECT_ROOT / "data/mocks/schemas/pass_lsg_reserve.json", True),
    (PROJECT_ROOT / "data/mocks/schemas/fail_missing_required_field.json", False),
]


def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Loads a JSON file and returns its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def governance_schema() -> Dict[str, Any]:
    """A pytest fixture that loads the governance JSON schema once per module."""
    schema_path = PROJECT_ROOT / "schemas" / "governance.schema.json"
    return load_json_file(schema_path)


@pytest.mark.parametrize("mock_path,should_be_valid", MOCK_FILES_TO_TEST)
def test_mock_validation(
    governance_schema: Dict[str, Any], mock_path: Path, should_be_valid: bool
):
    """
    Tests that mock data files either validate or fail to validate against
    the governance schema, as expected.
    """
    print(f"Testing: {mock_path.relative_to(PROJECT_ROOT)}")
    mock_data = load_json_file(mock_path)

    if should_be_valid:
        # Assert that validation succeeds without raising an error
        jsonschema.validate(instance=mock_data, schema=governance_schema)
    else:
        # Assert that a ValidationError is raised for invalid data
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=mock_data, schema=governance_schema)
        # Optional: print the error for context in the test output
        print(f"   -> Successfully caught expected error: {excinfo.value.message}")
