from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


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
    languages: List[str]
    best_seasons: List[Season] = Field(..., description="Best seasons to visit")


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
    languages: Optional[List[str]] = None
    best_seasons: Optional[List[Season]] = None


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
