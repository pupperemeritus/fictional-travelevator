from app.models.user import User, UserUpdate
from app.services.supabase_client import supabase_client_manager
from app.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
supabase_client = supabase_client_manager.get_client()


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=User)
async def update_user(
    user_update: UserUpdate, current_user: User = Depends(get_current_user)
):
    try:
        updated_user = (
            supabase_client.table("users")
            .update(user_update.dict(exclude_unset=True))
            .eq("id", current_user.id)
            .execute()
        )
        return User(**updated_user.data[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/me", status_code=204)
async def delete_user(current_user: User = Depends(get_current_user)):
    try:
        supabase_client.auth.admin.delete_user(current_user.id)
        supabase_client.table("users").delete().eq("id", current_user.id).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
