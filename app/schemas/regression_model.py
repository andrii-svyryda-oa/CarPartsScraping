from pydantic import BaseModel
from datetime import datetime
import uuid

class CreateRegressionModelIn(BaseModel):
    name: str
    target_variable: str
    feature_variables: list[str]
    coefficients: dict
    intercept: float
    r_squared: float
    mean_squared_error: float
    category_id: uuid.UUID
    last_trained_at: datetime
    training_data_count: int

class UpdateRegressionModelIn(BaseModel):
    name: str | None = None
    target_variable: str | None = None
    feature_variables: list[str] | None = None
    coefficients: dict | None = None
    intercept: float | None = None
    r_squared: float | None = None
    mean_squared_error: float | None = None
    category_id: uuid.UUID | None = None
    last_trained_at: datetime | None = None
    training_data_count: int | None = None

class RegressionModelOut(BaseModel):
    id: uuid.UUID
    name: str
    target_variable: str
    feature_variables: list[str]
    coefficients: dict
    intercept: float
    r_squared: float
    mean_squared_error: float
    category_id: uuid.UUID
    last_trained_at: datetime
    training_data_count: int 