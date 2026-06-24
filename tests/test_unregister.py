from urllib.parse import quote

import src.app as app_module


def signup_path(activity_name):
    return f"/activities/{quote(activity_name)}/signup"


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(signup_path(activity_name), params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_missing_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(signup_path(activity_name), params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_email_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-present@mergington.edu"

    # Act
    response = client.delete(signup_path(activity_name), params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student not signed up for this activity"


def test_signup_unregister_signup_flow_is_supported(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "rejoin@mergington.edu"

    # Act
    first_signup = client.post(signup_path(activity_name), params={"email": email})
    unregister = client.delete(signup_path(activity_name), params={"email": email})
    second_signup = client.post(signup_path(activity_name), params={"email": email})

    # Assert
    assert first_signup.status_code == 200
    assert unregister.status_code == 200
    assert second_signup.status_code == 200
    assert app_module.activities[activity_name]["participants"].count(email) == 1