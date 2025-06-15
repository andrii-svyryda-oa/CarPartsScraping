from pydantic import BaseModel
import uuid

class ScrapedPartDataBase(BaseModel):
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

class ScrapedPartDataCreate(ScrapedPartDataBase):
    part_id: uuid.UUID
    platform_id: uuid.UUID

class ScrapedPartDataUpdate(BaseModel):
    part_id: uuid.UUID | None = None
    platform_id: uuid.UUID | None = None
    url: str | None = None
    title_on_platform: str | None = None
    article_number: str | None = None
    price: float | None = None
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
