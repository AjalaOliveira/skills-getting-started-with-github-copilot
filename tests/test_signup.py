from urllib.parse import quote

import src.app as app_module


def signup_path(activity_name):
    return f"/activities/{quote(activity_name)}/signup"


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "alice@mergington.edu"

    # Act
    response = client.post(signup_path(activity_name), params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_missing_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "alice@mergington.edu"

    # Act
    response = client.post(signup_path(activity_name), params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(signup_path(activity_name), params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"