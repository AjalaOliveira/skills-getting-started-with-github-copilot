import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Ensure each test starts with a clean copy of in-memory activities."""
    original_activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def client():
    return TestClient(app_module.app)