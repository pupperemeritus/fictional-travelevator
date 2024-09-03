from typing import List

from app.models.activities import UserPreferences
from app.models.itinerary import Itinerary, ItineraryCreate, ItineraryUpdate
from app.models.user import User
from app.services.llm_service import llm_service
from app.services.supabase_client import supabase_client_manager
from app.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
supabase_client = supabase_client_manager.get_client()


@router.post("/", response_model=Itinerary)
async def create_itinerary(
    itinerary: ItineraryCreate, current_user: User = Depends(get_current_user)
):
    try:
        new_itinerary = (
            supabase_client.table("itineraries")
            .insert({**itinerary.dict(), "user_id": current_user.id})
            .execute()
        )
        return Itinerary(**new_itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Itinerary])
async def read_itineraries(current_user: User = Depends(get_current_user)):
    try:
        itineraries = (
            supabase_client.table("itineraries")
            .select("*")
            .eq("user_id", current_user.id)
            .execute()
        )
        return [Itinerary(**itinerary) for itinerary in itineraries.data]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{itinerary_id}", response_model=Itinerary)
async def read_itinerary(
    itinerary_id: str, current_user: User = Depends(get_current_user)
):
    try:
        itinerary = (
            supabase_client.table("itineraries")
            .select("*")
            .eq("id", itinerary_id)
            .eq("user_id", current_user.id)
            .execute()
        )
        if not itinerary.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        return Itinerary(**itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{itinerary_id}", response_model=Itinerary)
async def update_itinerary(
    itinerary_id: str,
    itinerary_update: ItineraryUpdate,
    current_user: User = Depends(get_current_user),
):
    try:
        updated_itinerary = (
            supabase_client.table("itineraries")
            .update(itinerary_update.dict(exclude_unset=True))
            .eq("id", itinerary_id)
            .eq("user_id", current_user.id)
            .execute()
        )
        if not updated_itinerary.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        return Itinerary(**updated_itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{itinerary_id}", status_code=204)
async def delete_itinerary(
    itinerary_id: str, current_user: User = Depends(get_current_user)
):
    try:
        deleted = (
            supabase_client.table("itineraries")
            .delete()
            .eq("id", itinerary_id)
            .eq("user_id", current_user.id)
            .execute()
        )
        if not deleted.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate", response_model=Itinerary)
async def generate_itinerary(
    user_preferences: UserPreferences,
    destinations: List[str],
    duration: int,
    current_user: User = Depends(get_current_user),
):
    try:
        itinerary = llm_service.generate_itinerary(
            user_preferences, destinations, duration
        )
        new_itinerary = (
            supabase_client.table("itineraries")
            .insert({**itinerary.dict(), "user_id": current_user.id})
            .execute()
        )
        return Itinerary(**new_itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=Itinerary)
async def create_itinerary(
    itinerary: ItineraryCreate, current_user: User = Depends(get_current_user)
):
    try:
        new_itinerary = (
            supabase_client.table("itineraries")
            .insert({**itinerary.dict(), "user_id": current_user.id})
            .execute()
        )
        return Itinerary(**new_itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
