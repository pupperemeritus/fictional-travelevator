import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/auth/login", json=data)
    return response.json()["access_token"]


def test_register_user(client):
    data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword",
    }
    response = client.post("/auth/register", json=data)
    print(response.status_code)
    print(response.json())  # Add this to inspect the response body
    assert response.status_code == 200


def test_login_user(client):
    data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/auth/login", params=data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert "email" in response.json()


def test_create_itinerary(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "title": "Test Itinerary",
        "start_date": "2023-06-01T00:00:00",
        "end_date": "2023-06-15T00:00:00",
        "user_id": "test_user_id",
        "total_budget": 5000,
        "destinations": [
            {
                "destination_id": "destination_id_1",
                "arrival_time": "2023-06-01T00:00:00",
                "departure_time": "2023-06-05T00:00:00",
            },
            {
                "destination_id": "destination_id_2",
                "arrival_time": "2023-06-05T00:00:00",
                "departure_time": "2023-06-10T00:00:00",
            },
        ],
    }
    response = client.post("/itineraries/", json=data, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_destinations(client):
    response = client.get("/destinations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_destination(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "name": "Test Destination",
        "country": "Test Country",
        "description": "This is a test destination.",
    }
    response = client.post("/destinations/", json=data, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_generate_itinerary(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "user_preferences": {
            "interests": ["hiking", "food"],
            "budget": 5000,
            "preferred_travel_style": "relaxed",
            "preferred_activities": ["hiking", "sightseeing"],
            "accessibility_needs": ["wheelchair accessible"],
        },
        "destinations": ["destination_id_1", "destination_id_2"],
    }
    response = client.post("/itineraries/generate", json=data, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_read_itineraries(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/itineraries/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_itinerary(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/itineraries/itinerary_id", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_update_itinerary(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"title": "Updated Itinerary", "total_budget": 6000}
    response = client.put("/itineraries/itinerary_id", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Itinerary"
    assert response.json()["total_budget"] == 6000


def test_delete_itinerary(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete("/itineraries/itinerary_id", headers=headers)
    assert response.status_code == 204


def test_read_destination(client):
    response = client.get("/destinations/destination_id")
    assert response.status_code == 200
    assert "id" in response.json()


def test_update_destination(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "name": "Updated Destination",
        "description": "This is an updated destination.",
    }
    response = client.put("/destinations/destination_id", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Destination"
    assert response.json()["description"] == "This is an updated destination."


def test_delete_destination(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete("/destinations/destination_id", headers=headers)
    assert response.status_code == 204


def test_update_user(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"full_name": "Updated User Name", "email": "updated@example.com"}
    response = client.put("/users/me", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated User Name"
    assert response.json()["email"] == "updated@example.com"


def test_delete_user(client):
    # Assume a valid access token is obtained from the login test
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 204


def test_validation_errors(client):
    # Test validation errors for various endpoints
    headers = {"Authorization": f"Bearer {auth_token}"}

    data = {"email": "invalid_email", "full_name": "", "password": "short"}
    response = client.post("/auth/register", json=data)
    assert response.status_code == 422
    assert "detail" in response.json()

    data = {"title": "", "start_date": "invalid_date", "total_budget": -100}
    response = client.post("/itineraries/", json=data, headers=headers)
    assert response.status_code == 422
    assert "detail" in response.json()

    data = {"name": "", "country": ""}
    response = client.post("/destinations/", json=data, headers=headers)
    assert response.status_code == 422
    assert "detail" in response.json()
