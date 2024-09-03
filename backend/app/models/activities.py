from datetime import datetime
from typing import List, Optional

from geopy.distance import geodesic
from pydantic import BaseModel, ConfigDict, Field


class Place(BaseModel):
    id: str
    name: str
    type: str  # 'city', 'state', or 'country'
    parent_id: Optional[str] = None
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class UserPreferences(BaseModel):
    interests: List[str] = Field(..., description="List of user's interests")
    budget: float = Field(..., ge=0, description="User's budget for the trip")
    preferred_travel_style: str = Field(
        ..., description="User's preferred travel style"
    )
    preferred_activities: List[str] = Field(
        ..., description="List of user's preferred activities"
    )
    accessibility_needs: Optional[List[str]] = Field(
        None, description="List of user's accessibility needs"
    )


class ActivityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: datetime
    end_time: datetime
    cost: float = Field(..., ge=0)
    tags: List[str] = Field(..., description="Tags describing the activity")
    place_id: str


class ActivityCreate(ActivityBase):
    itinerary_id: str


class ActivityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    cost: Optional[float] = Field(None, ge=0)
    tags: Optional[List[str]] = None


class ActivityInDB(ActivityBase):
    id: str
    itinerary_id: str

    model_config = ConfigDict(from_attributes=True)


class Activity(ActivityInDB):
    pass
