from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


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


class ItineraryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    start_date: datetime
    end_date: datetime
    user_id: str
    total_budget: float = Field(..., ge=0)
    destinations: List[DestinationInItinerary]


class ItineraryCreate(ItineraryBase):
    pass


class ItineraryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_budget: Optional[float] = Field(None, ge=0)
    destinations: Optional[List[DestinationInItinerary]] = None


class ItineraryInDB(ItineraryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Itinerary(ItineraryInDB):
    pass
