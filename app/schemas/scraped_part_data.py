from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
import uuid

class CreateScrapedPartDataIn(BaseModel):
    part_id: uuid.UUID
    platform_id: uuid.UUID
    url: str
    title_on_platform: str
    article_number: str
    price: Decimal
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

class UpdateScrapedPartDataIn(BaseModel):
    part_id: uuid.UUID | None = None
    platform_id: uuid.UUID | None = None
    url: str | None = None
    title_on_platform: str | None = None
    article_number: str | None = None
    price: Decimal | None = None
    availability_status: str | None = None
    delivery_days: int | None = None
    seller_name: str | None = None
    seller_rating: float | None = None
    seller_type: str | None = None
    location: str | None = None
    warranty_months: int | None = None
    reviews_count: int | None = None
    search_position: int | None = None
    images: list[str] | None = None

class ScrapedPartDataOut(BaseModel):
    id: uuid.UUID
    part_id: uuid.UUID
    platform_id: uuid.UUID
    url: str
    title_on_platform: str
    article_number: str
    price: Decimal
    availability_status: str
    delivery_days: int | None
    seller_name: str
    seller_rating: float | None
    seller_type: str
    location: str
    warranty_months: int | None
    reviews_count: int | None
    search_position: int
    images: list[str] | None
    scraped_at: datetime 