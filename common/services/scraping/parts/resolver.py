import common.services.scraping.parts.implementations # noqa
from common.services.scraping.parts.base import BasePartScraper, registered_scrapers
from typing import Type

def get_scraper(platform_name: str) -> Type[BasePartScraper] | None:
    return registered_scrapers.get(platform_name)
    