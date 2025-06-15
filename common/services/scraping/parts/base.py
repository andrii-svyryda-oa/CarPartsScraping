from abc import abstractmethod
from dataclasses import dataclass
from typing import Type
from common.database.models.car_model_platform import CarModelPlatform
from pydantic import BaseModel

from common.database.models.part_category import PartCategory

class ScrapedPart(BaseModel):
    url: str
    title_on_platform: str
    article_number: str
    price: float
    availability_status: str
    delivery_days: int | None = None
    seller_name: str
    seller_rating: float | None = None
    seller_type: str
    location: str
    warranty_months: int | None = None
    reviews_count: int | None = None
    search_position: int
    images: list[str] | None = None


@dataclass
class BasePartScraper:
    platform_url: str
    category: str
    pages: int = 10
    
    @abstractmethod
    async def __call__(self) -> list[ScrapedPart]:
        pass
    

registered_scrapers: dict[str, Type[BasePartScraper]] = {}


def implements_platform_scraper(platform_name: str):
    def decorator(cls):
        registered_scrapers[platform_name] = cls
        return cls

    return decorator
