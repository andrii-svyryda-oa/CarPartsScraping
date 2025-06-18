from pydantic import BaseModel
from datetime import datetime
import uuid

from common.services.regression.price_regression.predict import PricePredictionResult
from common.services.regression.price_regression.train import PricePredictionInput

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
    
class TrainRegressionModelIn(BaseModel):
    category_id: uuid.UUID
    name: str
    
class PricePredictionIn(PricePredictionInput):
    pass

class PricePredictionOut(PricePredictionResult):
    pass

class ModelStatsIn(BaseModel):
    min_reviews_count: int
    max_reviews_count: int
    min_search_position: int
    max_search_position: int
    manufacturers: list[str]
    platforms: list[str]
