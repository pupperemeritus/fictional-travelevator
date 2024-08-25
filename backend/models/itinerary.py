from typing import Optional, Sequence, List
from pydantic import BaseModel


class UserPreferences(BaseModel):
    user_id: str


class Activities(BaseModel):
    activity_id: str
    name: str
    cost: List[float]


class Destination(BaseModel):
    location_name: str
    location_activities: str
    latitude: float
    longitude: float
    activities: List[Activities]


class Itinerary(BaseModel):
    itinerary_id: str
    user_id: str
    destination_id: str
    itinerary_sequence: Sequence[Destination]
    itinerary_cost_minimum: float
    itinerary_cost_maximum: float


class Review(BaseModel):
    review_id: str
