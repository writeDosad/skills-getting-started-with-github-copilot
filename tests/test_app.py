"""Tests for the Mergington High School API"""

from fastapi.testclient import TestClient
from src import app as app_module


client = TestClient(app_module.app)


def test_get_activities_returns_200_with_chess_club():
    # Arrange
    expected_status = 200

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == expected_status
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant_and_returns_message():
    # Arrange
    activity_name = "Chess Club"
    email = "unique-signup-1@mergington.edu"
    expected_status = 200

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == expected_status
    assert "message" in response.json()
    assert email in response.json()["message"]


def test_duplicate_signup_returns_400_with_detail():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate-test@mergington.edu"

    # Act
    first = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    dup = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert first.status_code == 200
    assert dup.status_code == 400
    assert dup.json()["detail"] in [
        "Student already signed up for this activity",
        "Student is already registered for this activity",
    ]


def test_unregister_removes_participant_and_returns_message():
    # Arrange
    activity_name = "Chess Club"
    email = "to-unregister@mergington.edu"
    signup = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    assert signup.status_code == 200

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
