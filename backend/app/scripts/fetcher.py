import logging
import re
from typing import Any, Dict, List

import httpx
import wikipediaapi
from app.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RestCountriesWikipediaFetcher:
    def __init__(self):
        self.rest_countries_url = "https://restcountries.com/v3.1"
        self.wiki_api = wikipediaapi.Wikipedia(
            user_agent=f"FictionalTravelevator/1.0 ({settings.GITHUB_URL}; {settings.EMAIL} )",
            language="en",
        )
        self.http_client = httpx.Client(
            headers={
                "User-Agent": f"FictionalTravelevator/1.0 ({settings.GITHUB_URL}; {settings.EMAIL})"
            }
        )

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def fetch_countries(self) -> List[Dict[str, Any]]:
        try:
            response = self.http_client.get(f"{self.rest_countries_url}/all")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred while fetching countries: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def fetch_cities(self, country_code: str) -> List[Dict[str, Any]]:
        try:
            response = self.http_client.get(
                f"{self.rest_countries_url}/alpha/{country_code}"
            )
            response.raise_for_status()
            country_data = response.json()[0]
            return self.extract_cities(country_data)
        except httpx.HTTPError as e:
            logger.error(
                f"HTTP error occurred while fetching cities for {country_code}: {e}"
            )
            raise
        except (KeyError, IndexError) as e:
            logger.error(f"Error extracting city data for {country_code}: {e}")
            return []

    def extract_cities(self, country_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        cities = []
        if "capital" in country_data:
            cities.extend(
                [{"name": city, "is_capital": True} for city in country_data["capital"]]
            )
        if "cities" in country_data:
            cities.extend(
                [{"name": city, "is_capital": False} for city in country_data["cities"]]
            )
        return cities

    def fetch_wikipedia_info(self, city_name: str, country_name: str) -> Dict[str, Any]:
        page = self.wiki_api.page(city_name)

        if page.exists():
            if "disambiguation" in page.title:
                # Handling disambiguation: Search for the relevant country name in the disambiguation links
                links = page.links
                for link_title in links:
                    if re.search(
                        rf"\b{re.escape(country_name)}\b", link_title, re.IGNORECASE
                    ):
                        # Fetch the page for the matched link
                        country_page = self.wiki_api.page(link_title)
                        if country_page.exists():
                            return {
                                "summary": country_page.summary,  # First 500 characters of the summary
                                "url": country_page.fullurl,
                            }
                        else:
                            logger.warning(
                                f"No Wikipedia page found for disambiguation link: {link_title}"
                            )
                # If no matching page is found, return a message indicating so
                logger.warning(
                    f"No relevant Wikipedia page found for disambiguation page of {city_name}, {country_name}"
                )
                return {
                    "summary": "This page is a disambiguation page. No relevant city page found.",
                    "url": page.fullurl,
                }

            # If not a disambiguation page, return the standard page information
            return {
                "summary": page.summary,  # First 500 characters of the summary
                "url": page.fullurl,
            }
        else:
            logger.warning(f"No Wikipedia page found for {city_name}, {country_name}")
            return {"summary": "", "url": ""}

    def process_countries(self):
        countries = self.fetch_countries()
        for country in countries:
            country_name = country["name"]["common"]
            country_code = country["cca3"]
            logger.info(f"Processing country: {country_name}")

            cities = self.fetch_cities(country_code)
            for city in cities:
                city_name = city["name"]
                logger.info(f"Processing city: {city_name}")

                wiki_info = self.fetch_wikipedia_info(city_name, country_name)

                yield {
                    "name": city_name,
                    "country": country_name,
                    "is_capital": city["is_capital"],
                    "description": wiki_info["summary"],
                    "wikipedia_url": wiki_info["url"],
                    "country_data": country,
                }

    def __del__(self):
        self.http_client.close()
