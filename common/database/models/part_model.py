from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

part_model_association = Table(
    'part_models',
    Base.metadata,
    Column('car_model_id', UUID(as_uuid=True), ForeignKey('car_models.id'), primary_key=True),
    Column('part_id', UUID(as_uuid=True), ForeignKey('parts.id'), primary_key=True)
) 