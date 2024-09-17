from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Season(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


class DestinationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str
    currency: str
    local_currency: str = Field(..., min_length=1, max_length=50)
    languages: List[str]
    best_seasons: List[Season] = Field(..., description="Best seasons to visit")
    safety_rating: float = Field(
        ..., ge=0, le=10, description="Safety rating out of 10"
    )
    popular_events: List[str] = Field(
        default_factory=list, description="Annual events or festivals"
    )

    @field_validator("safety_rating")
    def validate_safety_rating(cls, v):
        return round(v, 1)


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    timezone: Optional[str] = None
    currency: Optional[str] = None
    local_currency: Optional[str] = Field(None, min_length=1, max_length=50)
    languages: Optional[List[str]] = None
    best_seasons: Optional[List[Season]] = None
    safety_rating: Optional[float] = Field(None, ge=0, le=10)
    popular_events: Optional[List[str]] = None


class DestinationInDB(DestinationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Destination(DestinationInDB):
    pass


class PlaceType(str, Enum):
    CITY = "city"
    STATE = "state"
    COUNTRY = "country"


class Place(BaseModel):
    id: str
    name: str
    type: PlaceType
    parent_id: Optional[str] = None
    latitude: float
    longitude: float
    population: Optional[int] = None
    region: Optional[str] = None
    continent: str

    model_config = ConfigDict(from_attributes=True)
