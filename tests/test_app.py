from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_data

client = TestClient(app)
original_activities = deepcopy(activities_data)


@pytest.fixture(autouse=True)
def reset_activities():
    activities_data.clear()
    activities_data.update(deepcopy(original_activities))
    yield


def test_get_activities_returns_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant():
    activity_name = quote("Chess Club")
    new_email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    assert response.status_code == 200
    assert new_email in activities_data["Chess Club"]["participants"]
    assert "signed up" in response.json()["message"].lower()


def test_duplicate_signup_returns_400():
    activity_name = quote("Chess Club")
    existing_email = activities_data["Chess Club"]["participants"][0]

    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_remove_participant():
    activity_name = quote("Chess Club")
    existing_email = activities_data["Chess Club"]["participants"][0]

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": existing_email})

    assert response.status_code == 200
    assert existing_email not in activities_data["Chess Club"]["participants"]
    assert "removed" in response.json()["message"].lower()


def test_remove_nonexistent_participant_returns_404():
    activity_name = quote("Chess Club")

    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": "missing@mergington.edu"}
    )

    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()
