import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Preserve initial state of activities for test isolation
INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities dictionary state before each test run."""
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)
