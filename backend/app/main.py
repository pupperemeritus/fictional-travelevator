from app.api import destinations, itineraries, users
from app.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Travel Itinerary API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(itineraries.router, prefix="/itineraries", tags=["Itineraries"])
app.include_router(destinations.router, prefix="/destinations", tags=["Destinations"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Travel Itinerary API"}
