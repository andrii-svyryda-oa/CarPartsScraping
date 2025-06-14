import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID, JSON
from .base import Base
import uuid

class RegressionModel(Base):
    __tablename__ = "regression_models"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    target_variable: Mapped[str] = mapped_column(String, nullable=False)
    feature_variables: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    coefficients: Mapped[dict] = mapped_column(JSON, nullable=False)
    intercept: Mapped[float] = mapped_column(Float, nullable=False)
    r_squared: Mapped[float] = mapped_column(Float, nullable=False)
    mean_squared_error: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("part_categories.id"), nullable=False)
    last_trained_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    training_data_count: Mapped[int] = mapped_column(Integer, nullable=False)
    
    category = relationship("PartCategory")