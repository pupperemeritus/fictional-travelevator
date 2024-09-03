import random

from app.models.destinations import Destination
from app.services.llm_service import llm_service
from app.services.supabase_client import supabase_client_manager
from app.services.vector_store import vector_store_service

supabase_client = supabase_client_manager.get_client()


def populate_destinations():
    destinations = supabase_client.table("destinations").select("*").execute()

    for destination in destinations.data:
        if not destination.get("description"):
            mock_data = llm_service.generate_mock_destination(
                destination["name"], destination["country"]
            )
            updated_destination = (
                supabase_client.table("destinations")
                .update(mock_data)
                .eq("id", destination["id"])
                .execute()
                .data[0]
            )
        else:
            updated_destination = destination

        vector_store_service.add_destination(Destination(**updated_destination))

    print(
        f"Updated and added {len(destinations.data)} destinations to the vector store."
    )


def generate_mock_users(num_users=100):
    for _ in range(num_users):
        user_data = {
            "email": f"user{random.randint(1000, 9999)}@example.com",
            "password": "password123",
            "full_name": f"Mock User {random.randint(1000, 9999)}",
        }
        supabase_client.auth.sign_up(user_data)

    print(f"Generated {num_users} mock users.")


def generate_mock_itineraries(num_itineraries=500):
    users = supabase_client.table("users").select("id").execute()
    destinations = supabase_client.table("destinations").select("*").execute()

    for _ in range(num_itineraries):
        user = random.choice(users.data)
        destination_count = random.randint(1, 3)
        selected_destinations = random.sample(destinations.data, destination_count)
        duration = random.randint(3, 14)
        budget = random.uniform(500, 5000)

        mock_itinerary = llm_service.generate_mock_itinerary(
            [dest["name"] for dest in selected_destinations], duration, budget
        )

        itinerary_data = {
            "user_id": user["id"],
            "title": mock_itinerary["title"],
            "start_date": "2024-01-01",
            "end_date": "2024-01-14",
            "total_budget": budget,
            "destinations": [
                {"destination_id": dest["id"]} for dest in selected_destinations
            ],
        }

        new_itinerary = (
            supabase_client.table("itineraries")
            .insert(itinerary_data)
            .execute()
            .data[0]
        )

        for activity in mock_itinerary["activities"]:
            activity_data = {
                "itinerary_id": new_itinerary["id"],
                "name": activity["name"],
                "description": activity["description"],
                "cost": activity["estimated_cost"],
                "start_time": "2024-01-01T09:00:00",
                "end_time": "2024-01-01T11:00:00",
            }
            supabase_client.table("activities").insert(activity_data).execute()

    print(f"Generated {num_itineraries} mock itineraries with activities.")


def main():
    populate_destinations()
    generate_mock_users()
    generate_mock_itineraries()


if __name__ == "__main__":
    main()
