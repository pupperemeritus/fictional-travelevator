from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TripStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DestinationInItinerary(BaseModel):
    destination_id: str
    arrival_time: datetime
    departure_time: datetime
    travel_time_from_previous: Optional[float] = Field(
        None, description="Travel time in hours from the previous destination"
    )
    travel_cost_from_previous: Optional[float] = Field(
        None, description="Travel cost in USD from the previous destination"
    )
    accommodation_id: Optional[str] = Field(
        None, description="ID of the accommodation at this destination"
    )


class ItineraryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    start_date: datetime
    end_date: datetime
    user_id: str
    total_budget: float = Field(..., ge=0)
    destinations: List[DestinationInItinerary]
    status: TripStatus = TripStatus.PLANNING


class ItineraryCreate(ItineraryBase):
    pass


class ItineraryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_budget: Optional[float] = Field(None, ge=0)
    destinations: Optional[List[DestinationInItinerary]] = None
    status: Optional[TripStatus] = None


class ItineraryInDB(ItineraryBase):
    id: str
    created_at: datetime
    updated_at: datetime
    total_cost: float = Field(0, description="Total estimated cost of the trip")
    rating: Optional[float] = Field(
        None, ge=1, le=5, description="User rating for the trip"
    )

    model_config = ConfigDict(from_attributes=True)


class Itinerary(ItineraryInDB):
    pass


class ItineraryFeedback(BaseModel):
    itinerary_id: str
    user_id: str
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)
