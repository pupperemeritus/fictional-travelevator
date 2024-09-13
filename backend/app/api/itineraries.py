from typing import List

from app.models.itinerary import Itinerary, ItineraryCreate, ItineraryUpdate
from app.models.user import UserPreferences
from app.services.llm_service import llm_service
from app.services.supabase_client import supabase_client_manager
from fastapi import APIRouter, HTTPException, Request
from geopy.distance import geodesic

router = APIRouter()
supabase_client = supabase_client_manager.get_client()


@router.post("/", response_model=Itinerary)
async def create_itinerary(itinerary: ItineraryCreate, request: Request):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        new_itinerary = (
            supabase_client.table("itineraries")
            .insert({**itinerary.model_dump(), "user_id": user_id})
            .execute()
        )
        return Itinerary(**new_itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Itinerary])
async def read_itineraries(request: Request):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        itineraries = (
            supabase_client.table("itineraries")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return [Itinerary(**itinerary) for itinerary in itineraries.data]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{itinerary_id}", response_model=Itinerary)
async def read_itinerary(itinerary_id: str, request: Request):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        itinerary = (
            supabase_client.table("itineraries")
            .select("*")
            .eq("id", itinerary_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not itinerary.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        return Itinerary(**itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{itinerary_id}", response_model=Itinerary)
async def update_itinerary(
    itinerary_id: str, itinerary_update: ItineraryUpdate, request: Request
):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        updated_itinerary = (
            supabase_client.table("itineraries")
            .update(itinerary_update.model_dump(exclude_unset=True))
            .eq("id", itinerary_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not updated_itinerary.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        return Itinerary(**updated_itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{itinerary_id}", status_code=204)
async def delete_itinerary(itinerary_id: str, request: Request):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        deleted = (
            supabase_client.table("itineraries")
            .delete()
            .eq("id", itinerary_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not deleted.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


router = APIRouter()
supabase_client = supabase_client_manager.get_client()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


def estimate_travel_cost(
    distance: float, base_cost: float, cost_per_km: float
) -> float:
    return base_cost + (distance * cost_per_km)


@router.post("/generate", response_model=Itinerary)
async def generate_itinerary(
    user_preferences: UserPreferences,
    destinations: List[str],
    duration: int,
    request: Request,
):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Fetch destination details
        destination_details = []
        for dest in destinations:
            details = (
                supabase_client.table("destinations")
                .select("*")
                .eq("name", dest)
                .execute()
            )
            if details.data:
                destination_details.append(details.data[0])
            else:
                raise HTTPException(
                    status_code=404, detail=f"Destination not found: {dest}"
                )

        # Generate itinerary using LLM
        itinerary = llm_service.generate_itinerary(
            user_preferences, destination_details, duration
        )

        # Calculate distances and costs
        total_distance = 0
        total_cost = 0
        for i in range(len(itinerary.destinations) - 1):
            d1 = itinerary.destinations[i]
            d2 = itinerary.destinations[i + 1]
            distance = calculate_distance(
                d1.latitude, d1.longitude, d2.latitude, d2.longitude
            )
            cost = estimate_travel_cost(distance, d2.base_travel_cost, d2.cost_per_km)
            total_distance += distance
            total_cost += cost
            d2.travel_time_from_previous = (
                distance / 100
            )  # Assuming average speed of 100 km/h
            d2.travel_cost_from_previous = cost

        itinerary.total_cost = total_cost

        # Save the itinerary
        new_itinerary = (
            supabase_client.table("itineraries")
            .insert({**itinerary.model_dump(), "user_id": user_id})
            .execute()
        )
        return Itinerary(**new_itinerary.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
