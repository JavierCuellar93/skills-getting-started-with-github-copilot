from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    email = "test-student@mergington.edu"

    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert unregister_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
