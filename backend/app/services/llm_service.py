from typing import Any, Dict, List

from app.models.destination import Destination
from app.models.itinerary import Itinerary
from app.models.user import UserPreferences
from app.services.vector_store import vector_store_service
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


class LLMService:
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.llm = OllamaLLM(model=model_name)

    def generate_destination_info(self, scraped_data: Dict[str, Any]) -> Destination:
        relevant_info = vector_store_service.get_relevant_info(
            scraped_data["name"], scraped_data["country"]
        )

        parser = PydanticOutputParser(pydantic_object=Destination)
        prompt = PromptTemplate(
            template="Generate comprehensive destination information for {name}, {country} based on the following scraped and relevant data:\n\nScraped Data: {scraped_data}\n\nRelevant Information: {relevant_info}\n\n{format_instructions}\n",
            input_variables=["name", "country", "scraped_data", "relevant_info"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        output = chain.run(
            name=scraped_data["name"],
            country=scraped_data["country"],
            scraped_data=scraped_data,
            relevant_info=relevant_info,
        )
        return Destination.model_validate_json(output)

    def generate_itinerary(
        self, user_preferences: UserPreferences, destinations: List[str], duration: int
    ) -> Itinerary:
        destinations_info = []
        for dest in destinations:
            dest_info = vector_store_service.get_destination_info(dest)
            destinations_info.append(dest_info)

        parser = PydanticOutputParser(pydantic_object=Itinerary)
        prompt = PromptTemplate(
            template="Generate a detailed itinerary for a {duration}-day trip to the following destinations: {destinations}\n\nUser Preferences: {user_preferences}\n\nDestination Information: {destinations_info}\n\nPlease create an itinerary that takes into account the user's preferences, the specific details of each destination, and ensures a logical and enjoyable travel sequence. Include specific activities, accommodations, and travel methods between destinations.\n\n{format_instructions}\n",
            input_variables=[
                "destinations",
                "duration",
                "user_preferences",
                "destinations_info",
            ],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        output = chain.run(
            destinations=", ".join(destinations),
            duration=duration,
            user_preferences=user_preferences.model_dump_json(),
            destinations_info=destinations_info,
        )
        return Itinerary.model_validate_json(output)


llm_service = LLMService()
