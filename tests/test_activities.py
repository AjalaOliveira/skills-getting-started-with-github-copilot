import src.app as app_module


def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in payload
    assert "description" in payload[expected_activity]
    assert "schedule" in payload[expected_activity]
    assert "max_participants" in payload[expected_activity]
    assert "participants" in payload[expected_activity]


def test_get_activities_reflects_current_in_memory_state(client):
    # Arrange
    activity_name = "Science Club"
    new_participant = "newstudent@mergington.edu"
    app_module.activities[activity_name]["participants"].append(new_participant)

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert new_participant in payload[activity_name]["participants"]