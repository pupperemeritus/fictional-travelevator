import pytest
from unittest.mock import Mock, patch
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService
from backend.app.models.destination import Destination
from backend.app.models.user import UserPreferences
from app.models.itinerary import Itinerary


@pytest.fixture
def llm_service():
    return LLMService()


@pytest.fixture
def vector_store_service():
    return VectorStoreService()


def test_generate_mock_destination(llm_service):
    destination = llm_service.generate_mock_destination("Paris", "France")
    assert isinstance(destination, Destination)
    assert destination.name == "Paris"
    assert destination.country == "France"


def test_generate_itinerary(llm_service):
    user_preferences = UserPreferences(
        user_id="test_user",
        interests=["history", "cuisine"],
        budget=1000.0,
        preferred_travel_style="relaxed",
        preferred_activities=["sightseeing", "dining"],
    )
    destinations = ["Paris", "Rome"]
    duration = 7

    itinerary = llm_service.generate_itinerary(user_preferences, destinations, duration)
    assert isinstance(itinerary, Itinerary)
    assert len(itinerary.destinations) == 2
    assert itinerary.start_date is not None
    assert itinerary.end_date is not None


def test_add_destination(vector_store_service):
    destination = Destination(
        id="test_id",
        name="Test City",
        country="Test Country",
        description="A beautiful test city",
        latitude=0.0,
        longitude=0.0,
        timezone="UTC",
        currency="USD",
        languages=["English"],
        best_seasons=["Summer"],
    )
    vector_store_service.add_destination(destination)
    # Assert that the destination was added successfully (this might require mocking the Chroma client)


def test_search_destinations(vector_store_service):
    results = vector_store_service.search_destinations("beautiful city")
    assert len(results) > 0
    # Assert that the results are relevant (this might require mocking the Chroma client)
