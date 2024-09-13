from typing import List
from fastapi import APIRouter, HTTPException, Request
from app.models.destination import Destination, DestinationCreate, DestinationUpdate
from app.services.supabase_client import supabase_client_manager
from app.services.vector_store import vector_store_service

router = APIRouter()
supabase_client = supabase_client_manager.get_client()


@router.post("/", response_model=Destination)
async def create_destination(destination: DestinationCreate, request: Request):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        new_destination = (
            supabase_client.table("destinations")
            .insert(destination.model_dump())
            .execute()
        )
        created_destination = Destination(**new_destination.data[0])
        vector_store_service.add_destination(created_destination)
        return created_destination
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
    destination_id: str, destination_update: DestinationUpdate, request: Request
):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        updated_destination = (
            supabase_client.table("destinations")
            .update(destination_update.model_dump(exclude_unset=True))
            .eq("id", destination_id)
            .execute()
        )
        if not updated_destination.data:
            raise HTTPException(status_code=404, detail="Destination not found")
        return Destination(**updated_destination.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{destination_id}", status_code=204)
async def delete_destination(destination_id: str, request: Request):
    try:
        user_id = request.headers.get("user-id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

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
