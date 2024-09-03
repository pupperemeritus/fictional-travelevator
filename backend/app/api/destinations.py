from typing import List

from app.models.destinations import Destination, DestinationCreate, DestinationUpdate
from app.models.user import User
from app.services.supabase_client import supabase_client_manager
from app.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
supabase_client = supabase_client_manager.get_client()


@router.post("/", response_model=Destination)
async def create_destination(
    destination: DestinationCreate, current_user: User = Depends(get_current_user)
):
    try:
        new_destination = (
            supabase_client.table("destinations").insert(destination.dict()).execute()
        )
        return Destination(**new_destination.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Destination])
async def read_destinations():
    try:
        destinations = supabase_client.table("destinations").select("*").execute()
        return [Destination(**destination) for destination in destinations.data]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{destination_id}", response_model=Destination)
async def read_destination(destination_id: str):
    try:
        destination = (
            supabase_client.table("destinations")
            .select("*")
            .eq("id", destination_id)
            .execute()
        )
        if not destination.data:
            raise HTTPException(status_code=404, detail="Destination not found")
        return Destination(**destination.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{destination_id}", response_model=Destination)
async def update_destination(
    destination_id: str,
    destination_update: DestinationUpdate,
    current_user: User = Depends(get_current_user),
):
    try:
        updated_destination = (
            supabase_client.table("destinations")
            .update(destination_update.dict(exclude_unset=True))
            .eq("id", destination_id)
            .execute()
        )
        if not updated_destination.data:
            raise HTTPException(status_code=404, detail="Destination not found")
        return Destination(**updated_destination.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{destination_id}", status_code=204)
async def delete_destination(
    destination_id: str, current_user: User = Depends(get_current_user)
):
    try:
        deleted = (
            supabase_client.table("destinations")
            .delete()
            .eq("id", destination_id)
            .execute()
        )
        if not deleted.data:
            raise HTTPException(status_code=404, detail="Destination not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
