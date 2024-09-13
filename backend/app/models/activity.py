from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ActivityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: datetime
    end_time: datetime
    cost: float = Field(..., ge=0)
    tags: List[str] = Field(..., description="Tags describing the activity")
    place_id: str
    accessibility_info: Optional[str] = Field(None, max_length=500)


class ActivityCreate(ActivityBase):
    itinerary_id: str


class ActivityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    cost: Optional[float] = Field(None, ge=0)
    tags: Optional[List[str]] = None
    accessibility_info: Optional[str] = Field(None, max_length=500)


class BookingStatus(str, Enum):
    NOT_BOOKED = "not_booked"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class ActivityInDB(ActivityBase):
    id: str
    itinerary_id: str
    booking_status: BookingStatus = BookingStatus.NOT_BOOKED
    user_rating: Optional[float] = Field(None, ge=1, le=5)
    user_review: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)


class Activity(ActivityInDB):
    pass


class TransportationType(str, Enum):
    WALKING = "walking"
    BICYCLE = "bicycle"
    CAR = "car"
    BUS = "bus"
    TRAIN = "train"
    PLANE = "plane"
    BOAT = "boat"


class Transportation(BaseModel):
    id: str
    type: TransportationType
    from_place_id: str
    to_place_id: str
    departure_time: datetime
    arrival_time: datetime
    cost: float
    description: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)


class AccommodationType(str, Enum):
    HOTEL = "hotel"
    HOSTEL = "hostel"
    APARTMENT = "apartment"
    CAMPING = "camping"
    RESORT = "resort"
    GUESTHOUSE = "guesthouse"


class Accommodation(BaseModel):
    id: str
    name: str
    place_id: str
    type: AccommodationType
    address: str
    check_in_time: datetime
    check_out_time: datetime
    cost_per_night: float
    description: Optional[str] = Field(None, max_length=500)
    amenities: List[str]

    model_config = ConfigDict(from_attributes=True)


class Weather(BaseModel):
    place_id: str
    date: datetime
    temperature_high: float
    temperature_low: float
    precipitation_chance: float
    description: str

    model_config = ConfigDict(from_attributes=True)


class CurrencyExchange(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


class Language(BaseModel):
    code: str
    name: str
    common_phrases: dict[str, str]  # e.g., {"hello": "Bonjour", "thank you": "Merci"}

    model_config = ConfigDict(from_attributes=True)
