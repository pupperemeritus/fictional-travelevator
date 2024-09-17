from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TripStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ItineraryTheme(str, Enum):
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    RELAXATION = "relaxation"
    FOOD_AND_WINE = "food_and_wine"
    HISTORICAL = "historical"
    NATURE = "nature"


class FlexibilityLevel(str, Enum):
    RIGID = "rigid"
    FLEXIBLE = "flexible"
    VERY_FLEXIBLE = "very_flexible"


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
    theme: ItineraryTheme = Field(..., description="Theme of the itinerary")
    flexibility: FlexibilityLevel = Field(
        ..., description="How flexible the itinerary is"
    )
    sustainability_score: float = Field(
        ..., ge=0, le=10, description="Eco-friendliness rating out of 10"
    )

    @field_validator("end_date")
    def end_date_after_start_date(cls, v, values):
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v

    @field_validator("sustainability_score")
    def validate_sustainability_score(cls, v):
        return round(v, 1)


class ItineraryCreate(ItineraryBase):
    pass


class ItineraryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_budget: Optional[float] = Field(None, ge=0)
    destinations: Optional[List[DestinationInItinerary]] = None
    status: Optional[TripStatus] = None
    theme: Optional[ItineraryTheme] = None
    flexibility: Optional[FlexibilityLevel] = None
    sustainability_score: Optional[float] = Field(None, ge=0, le=10)


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
