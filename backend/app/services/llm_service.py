import json
from typing import Any, Dict, List

from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from pydantic import BaseModel, Field


class Destination(BaseModel):
    description: str = Field(description="A brief overview of the destination")
    popular_attractions: List[str] = Field(
        description="List of 3-5 popular attractions"
    )
    average_cost_per_day: float = Field(description="Average cost per day in USD")
    best_time_to_visit: str = Field(
        description="Brief description of the best time to visit"
    )


class Activity(BaseModel):
    name: str = Field(description="Name of the activity")
    description: str = Field(description="Brief description of the activity")
    estimated_cost: float = Field(description="Estimated cost of the activity in USD")


class Itinerary(BaseModel):
    title: str = Field(description="A catchy title for the itinerary")
    activities: List[Activity] = Field(
        description="List of activities in the itinerary"
    )


class LLMService:
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.llm = OllamaLLM(model=model_name)

    def generate_mock_destination(self, name: str, country: str) -> Dict[str, Any]:
        parser = PydanticOutputParser(pydantic_object=Destination)
        prompt = PromptTemplate(
            template="Generate a mock destination data for {name}, {country}.\n{format_instructions}\n",
            input_variables=["name", "country"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        output = chain.run(name=name, country=country)
        return json.loads(output)

    def generate_mock_itinerary(
        self, destination: str, duration: int, budget: float
    ) -> Dict[str, Any]:
        parser = PydanticOutputParser(pydantic_object=Itinerary)
        prompt = PromptTemplate(
            template="Generate a mock itinerary for a {duration}-day trip to {destination} with a budget of ${budget}.\n{format_instructions}\n",
            input_variables=["destination", "duration", "budget"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        output = chain.run(destination=destination, duration=duration, budget=budget)
        return json.loads(output)


llm_service = LLMService()
