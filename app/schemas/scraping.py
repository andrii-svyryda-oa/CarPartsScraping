from pydantic import BaseModel


class ScrapingStartIn(BaseModel):
    platforms_ids: list[str]
    car_model_id: str
    category_ids: list[str]
    pages: int
