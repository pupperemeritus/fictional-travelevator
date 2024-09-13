from app.main import app
from app.models.itinerary import ItineraryCreate, ItineraryUpdate
from fastapi.testclient import TestClient

from backend.app.models.destination import DestinationCreate, DestinationUpdate
from backend.app.models.user import UserPreferences

client = TestClient(app, base_url="http://localhost:8000")


def test_create_destination():
    destination_data = {
        "name": "Test City",
        "country": "Test Country",
        "description": "A beautiful test city",
        "latitude": 0.0,
        "longitude": 0.0,
        "timezone": "UTC",
        "currency": "USD",
        "languages": ["English"],
        "best_seasons": ["Summer"],
    }
    response = client.post(
        "/destinations/", json=destination_data, headers={"user-id": "test_user"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test City"


def test_read_destinations():
    response = client.get("/destinations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_destination():
    # Assume we have a destination with id "test_id"
    response = client.get("/destinations/test_id")
    assert response.status_code == 200
    assert response.json()["id"] == "test_id"


def test_update_destination():
    update_data = {"description": "Updated description"}
    response = client.put(
        "/destinations/test_id", json=update_data, headers={"user-id": "test_user"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"


def test_delete_destination():
    response = client.delete("/destinations/test_id", headers={"user-id": "test_user"})
    assert response.status_code == 204


def test_create_itinerary():
    itinerary_data = {
        "title": "Test Itinerary",
        "start_date": "2023-06-01T00:00:00Z",
        "end_date": "2023-06-07T00:00:00Z",
        "total_budget": 1000.0,
        "destinations": [],
    }
    response = client.post(
        "/itineraries/", json=itinerary_data, headers={"user-id": "test_user"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Itinerary"


def test_read_itineraries():
    response = client.get("/itineraries/", headers={"user-id": "test_user"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_itinerary():
    # Assume we have an itinerary with id "test_id"
    response = client.get("/itineraries/test_id", headers={"user-id": "test_user"})
    assert response.status_code == 200
    assert response.json()["id"] == "test_id"


def test_update_itinerary():
    update_data = {"title": "Updated Itinerary"}
    response = client.put(
        "/itineraries/test_id", json=update_data, headers={"user-id": "test_user"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Itinerary"


def test_delete_itinerary():
    response = client.delete("/itineraries/test_id", headers={"user-id": "test_user"})
    assert response.status_code == 204


def test_generate_itinerary():
    user_preferences = {
        "user_id": "test_user",
        "interests": ["history", "cuisine"],
        "budget": 1000.0,
        "preferred_travel_style": "relaxed",
        "preferred_activities": ["sightseeing", "dining"],
    }
    destinations = ["Paris", "Rome"]
    duration = 7
    response = client.post(
        "/itineraries/generate",
        json={
            "user_preferences": user_preferences,
            "destinations": destinations,
            "duration": duration,
        },
        headers={"user-id": "test_user"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "title" in response.json()
    assert "destinations" in response.json()
