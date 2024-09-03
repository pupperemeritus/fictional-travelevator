import scrapy
from app.models.destinations import Destination
from app.services.supabase_client import supabase_client_manager
from app.services.vector_store import vector_store_service
from scrapy.crawler import CrawlerProcess


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

    def process_item(self, item, spider):
        destination = self.supabase.table("destinations").insert(item).execute().data[0]
        vector_store_service.add_destination(Destination(**destination))
        return item


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


if __name__ == "__main__":
    main()
