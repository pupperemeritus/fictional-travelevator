import random

from app.services.llm_service import llm_service
from app.services.supabase_client import supabase_client_manager
from app.utils import calculate_distance, estimate_travel_cost


def generate_mock_itineraries(num_itineraries=100):
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

        total_distance, total_cost = 0, 0
        for i in range(len(itinerary.destinations) - 1):
            d1, d2 = itinerary.destinations[i], itinerary.destinations[i + 1]
            distance = calculate_distance(
                d1.latitude, d1.longitude, d2.latitude, d2.longitude
            )
            cost = estimate_travel_cost(distance)
            total_distance += distance
            total_cost += cost
            d2.travel_time_from_previous = distance / 100
            d2.travel_cost_from_previous = cost

        itinerary.total_cost = total_cost

        supabase.table("itineraries").insert(itinerary.model_dump()).execute()
