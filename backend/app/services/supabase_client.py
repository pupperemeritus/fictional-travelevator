import httpx
from app.config import settings
from supabase import Client, create_client


class SupabaseClientManager:
    def __init__(self):
        self.client = None

    def get_client(self) -> Client:
        if self.client is None:
            self.client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY,
            )
        return self.client


supabase_client_manager = SupabaseClientManager()
