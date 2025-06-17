import numpy as np
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import List

from common.database.models.regression_model import RegressionModel
from common.services.regression.price_regression.train import PricePredictionInput

class PricePredictionResult(BaseModel):
    predicted_value: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    model_r_squared: float
    model_version: str

class PriceRegressionPredictor:
    scaler: StandardScaler
    label_encoders: dict[str, LabelEncoder]
    model: RegressionModel
    
    def __init__(self, model: RegressionModel):
        preprocessing = model.preprocessing_params
        scaler = StandardScaler()
        scaler.mean_ = np.array(preprocessing['scaler_mean'])
        scaler.scale_ = np.array(preprocessing['scaler_scale'])
                
        label_encoders = {}
        
        for feature, classes in preprocessing['label_encoders'].items():
            le = LabelEncoder()
            le.classes_ = np.array(classes)
            label_encoders[feature] = le
            
        self.scaler = scaler
        self.label_encoders = label_encoders
        self.model = model
        
    def predict_price(self, input: PricePredictionInput) -> PricePredictionResult:
        input_dict = input.model_dump()
        
        encoded_features = []
        feature_names = self.model.preprocessing_params['feature_names']
        
        for feature in feature_names:
            if feature.endswith('_encoded'):
                original_feature = feature.replace('_encoded', '')
                if original_feature in self.label_encoders:
                    value = input_dict.get(original_feature)
                    if value in self.label_encoders[original_feature].classes_:
                        encoded_value = self.label_encoders[original_feature].transform([value])[0]
                    else:
                        encoded_value = 0
                    encoded_features.append(encoded_value)
            else:
                encoded_features.append(input_dict.get(feature, 0))
        
        features_array = np.array(encoded_features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)
        
        features_with_const = np.concatenate([[1], features_scaled[0]])
        
        coefficients = self.model.coefficients
        prediction_log = sum(
            coefficients[key] * features_with_const[i] 
            for i, key in enumerate(coefficients.keys())
        )
        
        prediction = np.expm1(prediction_log)
        
        std_error = np.sqrt(self.model.mean_squared_error)
        confidence_interval = 1.96 * std_error 
        
        return PricePredictionResult(
            predicted_value=float(prediction),
            confidence_interval_lower=float(max(0, prediction - confidence_interval)),
            confidence_interval_upper=float(prediction + confidence_interval),
            model_r_squared=self.model.r_squared,
            model_version=self.model.model_version
        )
        
    def predict_price_multiple(self, model: RegressionModel, inputs: List[PricePredictionInput]) -> List[PricePredictionResult]:
        predictions = []

        for input in inputs:
            predictions.append(self.predict_price(model, input))
            
        return predictions
    