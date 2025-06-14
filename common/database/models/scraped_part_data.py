from sqlalchemy import String, DateTime, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.types import DECIMAL
from sqlalchemy.sql import func
from .base import Base
import uuid

class ScrapedPartData(Base):
    __tablename__ = "scraped_part_data"
    
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    part_id = mapped_column(UUID(as_uuid=True), ForeignKey("parts.id"), nullable=False)
    platform_id = mapped_column(UUID(as_uuid=True), ForeignKey("platforms.id"), nullable=False)
    url = mapped_column(Text, nullable=False)
    title_on_platform = mapped_column(String, nullable=False)
    article_number = mapped_column(String, nullable=False)
    price = mapped_column(DECIMAL(precision=10, scale=2), nullable=False)
    availability_status = mapped_column(String, nullable=False)
    delivery_days = mapped_column(Integer, nullable=True)
    seller_name = mapped_column(String, nullable=False)
    seller_rating = mapped_column(Float, nullable=True)
    seller_type = mapped_column(String, nullable=False)
    location = mapped_column(String, nullable=False)
    warranty_months = mapped_column(Integer, nullable=True)
    reviews_count = mapped_column(Integer, nullable=True)
    search_position = mapped_column(Integer, nullable=False)
    images = mapped_column(JSON, nullable=True)
    scraped_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    part = relationship("Part")
    platform = relationship("Platform")
