import math
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

import httpx
import scrapy
from app.models.destination import (
    Destination,
    DestinationCreate,
    Place,
    PlaceType,
    Season,
)
from app.services.llm_service import llm_service
from app.services.supabase_client import supabase_client_manager
from app.services.vector_store import vector_store_service
from geopy.distance import geodesic
from scrapy.crawler import CrawlerProcess

OPENWEATHERMAP_API_KEY = "your_openweathermap_api_key"
RESTCOUNTRIES_API_URL = "https://restcountries.com/v3.1"


class WikipediaCitiesSpider(scrapy.Spider):
    name = "wikipedia_cities"
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_city_listings_by_country",
        "https://en.wikipedia.org/wiki/List_of_towns",
    ]

    def parse(self, response):
        content = response.css("div.mw-parser-output")
        links = content.css("a::attr(href)").getall()

        for link in links:
            if link.startswith("/wiki/List_of_cities_in_") or link.startswith(
                "/wiki/List_of_towns_in_"
            ):
                yield response.follow(link, callback=self.parse_country_page)

    def parse_country_page(self, response):
        country_name = (
            response.css("h1#firstHeading::text")
            .get()
            .split("List of cities in ")[-1]
            .split("List of towns in ")[-1]
        )
        content = response.css("div.mw-parser-output")
        links = content.css("a::attr(href)").getall()

        for link in links:
            if link.startswith("/wiki/"):
                yield response.follow(
                    link, callback=self.parse_city_page, meta={"country": country_name}
                )

    def parse_city_page(self, response):
        country_name = response.meta["country"]
        city_name = response.css("h1#firstHeading::text").get()
        description = response.css("div.mw-parser-output p::text").get()

        if city_name and description:
            yield {
                "name": city_name.strip(),
                "country": country_name.strip(),
                "description": description.strip(),
            }


class SupabaseDestinationsPipeline:
    def __init__(self):
        self.supabase = supabase_client_manager.get_client()

    def get_country_info(self, country_name: str) -> Dict[str, Any]:
        url = f"{RESTCOUNTRIES_API_URL}/name/{country_name}"
        response = httpx.get(url)
        if response.status_code == 200:
            country_data = response.json()[0]
            return {
                "currency": list(country_data["currencies"].keys())[0],
                "languages": list(country_data["languages"].values()),
                "latitude": country_data["latlng"][0],
                "longitude": country_data["latlng"][1],
                "timezone": country_data["timezones"][0],
                "continent": country_data["region"],
            }
        return {}

    def get_weather_info(self, lat: float, lon: float) -> Dict[str, Any]:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}"
        response = httpx.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return {
                "temperature": weather_data["main"]["temp"]
                - 273.15,  # Convert to Celsius
                "description": weather_data["weather"][0]["description"],
            }
        return {}

    def determine_best_seasons(self, lat: float) -> List[Season]:
        if abs(lat) < 23.5:  # Tropical
            return [Season.SPRING, Season.AUTUMN, Season.WINTER]
        elif 23.5 <= abs(lat) < 66.5:  # Temperate
            return [Season.SPRING, Season.SUMMER, Season.AUTUMN]
        else:  # Polar
            return [Season.SUMMER]

    def process_item(self, item: Dict[str, Any], spider):
        country_info = self.get_country_info(item["country"])
        weather_info = self.get_weather_info(
            country_info["latitude"], country_info["longitude"]
        )

        destination_create = DestinationCreate(
            name=item["name"],
            country=item["country"],
            description=item["description"],
            latitude=country_info["latitude"],
            longitude=country_info["longitude"],
            timezone=country_info["timezone"],
            currency=country_info["currency"],
            languages=country_info["languages"],
            best_seasons=self.determine_best_seasons(country_info["latitude"]),
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

        # Store in vector store
        destination_obj = Destination(**destination)
        vector_store_service.add_destination(destination_obj)

        # Generate mock data using LLM
        mock_destination = llm_service.generate_mock_destination(
            item["name"], item["country"]
        )

        # Update destination with mock data
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


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


def estimate_travel_cost(distance: float) -> float:
    # Simple cost estimation based on distance
    base_cost = 50  # Base cost in USD
    cost_per_km = 0.1  # Cost per kilometer in USD
    return base_cost + (distance * cost_per_km)


def generate_mock_itineraries(num_itineraries: int = 100):
    supabase = supabase_client_manager.get_client()
    destinations = supabase.table("destinations").select("*").execute().data

    for _ in range(num_itineraries):
        num_destinations = random.randint(2, 5)
        selected_destinations = random.sample(destinations, num_destinations)
        duration = random.randint(7, 21)

        user_preferences = {
            "interests": random.sample(
                ["culture", "nature", "food", "history", "adventure"], 3
            ),
            "budget": random.uniform(1000, 5000),
            "preferred_travel_style": random.choice(["luxury", "budget", "mid-range"]),
            "preferred_activities": random.sample(
                ["sightseeing", "hiking", "shopping", "relaxing", "nightlife"], 3
            ),
            "preferred_transportation": random.sample(
                ["any", "car", "public_transport", "plane"], 2
            ),
        }

        itinerary = llm_service.generate_itinerary(
            user_preferences, [d["name"] for d in selected_destinations], duration
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
            cost = estimate_travel_cost(distance)
            total_distance += distance
            total_cost += cost
            d2.travel_time_from_previous = (
                distance / 100
            )  # Assuming average speed of 100 km/h
            d2.travel_cost_from_previous = cost

        itinerary.total_cost = total_cost

        # Store itinerary in Supabase
        supabase.table("itineraries").insert(itinerary.model_dump()).execute()


def main():
    process = CrawlerProcess(
        settings={
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "ITEM_PIPELINES": {
                "__main__.SupabaseDestinationsPipeline": 300,
            },
            "LOG_LEVEL": "INFO",
        }
    )

    process.crawl(WikipediaCitiesSpider)
    process.start()

    # Generate mock itineraries after scraping is complete
    generate_mock_itineraries()


if __name__ == "__main__":
    main()
