import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add the project root to the Python path.
# This allows tests to import modules from the 'app' directory as 'app.xxx'.
# The project root is assumed to be the parent directory of the 'tests' directory.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def client(monkeypatch):
    """A TestClient fixture that imports the app after the environment is set."""
    from tests.mocks import MockPocketBaseClient

    # Monkeypatch the real PocketBase client with our mock version
    # This ensures that any test using this fixture will not make real HTTP calls.
    monkeypatch.setattr("app.audits.impact.pb_client", MockPocketBaseClient())

    from app.main import app  # Import here to ensure SCHEMA_DIR is set

    with TestClient(app) as c:
        yield c