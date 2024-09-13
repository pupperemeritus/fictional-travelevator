from app.models.user import User, UserUpdate
from app.services.supabase_client import supabase_client_manager
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()
supabase_client = supabase_client_manager.get_client()


@router.get("/me")
async def read_users_me(request: Request):
    user_id = request.headers.get("user-id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"id": user_id}
