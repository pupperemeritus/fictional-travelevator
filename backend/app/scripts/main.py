import logging

import colorlog
from app.scripts.fetcher import RestCountriesWikipediaFetcher
from app.services.llm_service import llm_service
from app.services.supabase_client import supabase_client_manager
from app.services.vector_store import vector_store_service

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    fetcher = RestCountriesWikipediaFetcher()
    supabase = supabase_client_manager.get_client()

    for item in fetcher.process_countries():
        try:
            # Store scraped data in vector store
            vector_store_service.add_scraped_data(item)

            # Generate destination info using LLM and vector store
            destination_info = llm_service.generate_destination_info(item)

            # Store in database
            new_destination = (
                supabase.table("destinations")
                .insert(destination_info.model_dump())
                .execute()
            )

            if new_destination.data:
                logger.info(
                    f"Successfully processed and stored: {item['name']}, {item['country']}"
                )
            else:
                logger.warning(f"Failed to process: {item['name']}, {item['country']}")
        except Exception as e:
            logger.error(
                f"Error in main loop for {item['name']}, {item['country']}: {e}"
            )


if __name__ == "__main__":
    main()
