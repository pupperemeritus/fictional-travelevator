from app.models.user import User, UserCreate
from app.services.supabase_client import supabase_client_manager
from app.utils.security import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
supabase_client = supabase_client_manager.get_client()

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    try:
        response = supabase_client.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        new_user = response.user
        # Add additional user data to the user table
        supabase_client.table("users").insert(
            {"id": new_user.id, "email": new_user.email, "full_name": user.full_name}
        ).execute()
        return User(**new_user.dict(), full_name=user.full_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(email: str, password: str):
    try:
        response = supabase_client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        access_token = create_access_token(data={"sub": response.user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Incorrect email or password")


@router.get("/me", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = supabase_client.auth.get_user(token)
        return User(**user.dict())
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
