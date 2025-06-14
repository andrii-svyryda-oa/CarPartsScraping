from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class RegressionModelBase(BaseModel):
    name: str
    target_variable: str
    feature_variables: list[str]
    coefficients: dict
    intercept: float
    r_squared: float
    mean_squared_error: float
    training_data_count: int

class RegressionModelCreate(RegressionModelBase):
    category_id: uuid.UUID
    last_trained_at: datetime

class RegressionModelUpdate(BaseModel):
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

class RegressionModelResponse(RegressionModelBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    category_id: uuid.UUID
    last_trained_at: datetime 