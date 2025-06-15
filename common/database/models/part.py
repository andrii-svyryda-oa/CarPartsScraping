import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
from .base import Base
import uuid

class Part(Base):
    __tablename__ = "parts"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oem_number: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("part_categories.id"), nullable=False)
    manufacturer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("part_manufacturers.id"), nullable=False)
    specifications: Mapped[dict] = mapped_column(JSON, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    category = relationship("PartCategory")
    manufacturer = relationship("PartManufacturer")
    car_models = relationship("CarModel", secondary="part_models", back_populates="parts")
    