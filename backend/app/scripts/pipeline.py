import random

from app.models.destination import Destination, DestinationCreate, Place, PlaceType
from app.services.llm_service import llm_service
from app.services.supabase_client import supabase_client_manager
from app.services.vector_store import vector_store_service
from app.utils import determine_best_seasons, get_country_info, get_weather_info


class SupabaseDestinationsPipeline:
    def __init__(self):
        self.supabase = supabase_client_manager.get_client()

    def process_item(self, item, spider):
        country_info = get_country_info(item["country"])
        weather_info = get_weather_info(
            country_info["latitude"], country_info["longitude"]
        )

        # Destination Creation
        destination_create = DestinationCreate(
            name=item["name"],
            country=item["country"],
            description=item["description"],
            latitude=country_info["latitude"],
            longitude=country_info["longitude"],
            timezone=country_info["timezone"],
            currency=country_info["currency"],
            languages=country_info["languages"],
            best_seasons=determine_best_seasons(country_info["latitude"]),
        )

        destination = (
            self.supabase.table("destinations")
            .insert(destination_create.model_dump())
            .execute()
            .data[0]
        )

        place = Place(
            id=destination["id"],
            name=item["name"],
            type=PlaceType.CITY,
            parent_id=None,
            latitude=destination["latitude"],
            longitude=destination["longitude"],
            population=random.randint(10000, 1000000),
            region=item["country"],
            continent=country_info["continent"],
        )

        self.supabase.table("places").insert(place.model_dump()).execute()

        # Store in vector store and update mock data
        destination_obj = Destination(**destination)
        vector_store_service.add_destination(destination_obj)
        mock_destination = llm_service.generate_mock_destination(
            item["name"], item["country"]
        )

        updated_destination = (
            self.supabase.table("destinations")
            .update(
                {
                    "description": mock_destination.description,
                    "best_seasons": mock_destination.best_seasons,
                }
            )
            .eq("id", destination["id"])
            .execute()
            .data[0]
        )

        return updated_destination
