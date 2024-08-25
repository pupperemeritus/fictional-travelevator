from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.user.user_auth import authenticate_user_middleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def authenticate_user(request: Request, call_next):
    authenticate_user_middleware(request, call_next)
