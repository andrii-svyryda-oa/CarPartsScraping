import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base
import uuid

class CarModel(Base):
    __tablename__ = "car_models"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("car_brands.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    year_from: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    year_to: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    body_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    brand = relationship("CarBrand", back_populates="models")
    parts = relationship("Part", secondary="part_models", back_populates="car_models")
