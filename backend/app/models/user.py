from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    pass


class UserPreferences(BaseModel):
    user_id: str
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
    preferred_transportation: List[str] = Field(
        default=["any"], description="Preferred modes of transportation"
    )
    dietary_restrictions: Optional[List[str]] = Field(
        None, description="List of dietary restrictions"
    )
    language_preferences: Optional[List[str]] = Field(
        None, description="Preferred languages for communication"
    )
    max_travel_time: Optional[float] = Field(
        None,
        description="Maximum preferred travel time between destinations (in hours)",
    )

    model_config = ConfigDict(from_attributes=True)
