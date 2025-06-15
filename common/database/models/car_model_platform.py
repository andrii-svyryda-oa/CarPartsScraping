import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base
import uuid

class CarModelPlatform(Base):
    __tablename__ = "car_model_platforms"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    car_model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("car_models.id"), nullable=False)
    platform_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("platforms.id"), nullable=False)
    platform_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    car_model = relationship("CarModel")
    platform = relationship("Platform")
