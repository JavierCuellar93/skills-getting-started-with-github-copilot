import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    # Arrange
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))

    with TestClient(app_module.app) as test_client:
        yield test_client


def test_get_activities_returns_activity_list(client):
    # Arrange
    # The fixture has already populated the in-memory app state.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"]


def test_signup_for_activity(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    first_response = client.post(f"/activities/Chess Club/signup?email={email}")
    second_response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_from_activity(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    unregister_response = client.delete(f"/activities/Chess Club/participants/{email}")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
