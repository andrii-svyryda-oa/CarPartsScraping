from datetime import datetime
import pandas as pd
import numpy as np
from pydantic import BaseModel
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from typing import List
import uuid

from common.database.schemas.regression_model import RegressionModelCreate

class PricePredictionInput(BaseModel):
    platform: str
    reviews_count: int
    search_position: int
    manufacturer: str
    
    
class PricePredictionTrainingInput(PricePredictionInput):
    price: float

class PriceRegressionTrainer:
    scaler: StandardScaler
    label_encoders: dict[str, LabelEncoder]
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
    
    def _prepare_features(self, df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], dict[str, LabelEncoder]]:
        prepared_data = df.copy()
        
        categorical_features = ['platform', 'manufacturer']
        numeric_features = ['reviews_count', 'search_position']

        feature_variables = categorical_features + numeric_features
        
        label_encoders = {}
        
        for cat_feature in categorical_features:
            if cat_feature in prepared_data.columns:
                le = LabelEncoder()
                prepared_data[f'{cat_feature}_encoded'] = le.fit_transform(prepared_data[cat_feature])
                label_encoders[cat_feature] = le
        
        final_features = []
        for feature in feature_variables:
            if feature in categorical_features:
                final_features.append(f'{feature}_encoded')
            else:
                final_features.append(feature)
        
        return prepared_data[final_features], final_features, label_encoders
    
    def train_regression_model(
        self, 
        name: str,
        category_id: uuid.UUID,
        training_records: List[PricePredictionTrainingInput]
    ) -> RegressionModelCreate:
        data = pd.DataFrame([record.model_dump() for record in training_records])
            
        scaler = StandardScaler()
        
        X, feature_names, label_encoders = self._prepare_features(data)
        
        y = np.log1p(data['price'])
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        X_train_sm = sm.add_constant(X_train_scaled)
        X_test_sm = sm.add_constant(X_test_scaled)
        
        model = sm.OLS(y_train, X_train_sm).fit()
        
        y_pred_test = model.predict(X_test_sm)
        
        mse = np.mean((np.expm1(y_test) - np.expm1(y_pred_test))**2)
        
        feature_importance = {}
        for i, feature in enumerate(['intercept'] + feature_names):
            if feature != 'intercept':
                importance = abs(model.tvalues[i]) / sum(abs(model.tvalues[1:]))
                feature_importance[feature] = float(importance)
                
        return RegressionModelCreate(
            name=name,
            target_variable="price",
            feature_variables=feature_names,
            coefficients=dict(zip(['intercept'] + feature_names, model.params.tolist())),
            intercept=float(model.params[0]),
            r_squared=float(model.rsquared),
            mean_squared_error=float(mse),
            category_id=category_id,
            training_data_count=len(X_train),
            preprocessing_params={
                'scaler_mean': scaler.mean_.tolist(),
                'scaler_scale': scaler.scale_.tolist(),
                'label_encoders': {k: v.classes_.tolist() for k, v in label_encoders.items()},
                'feature_names': feature_names
            },
            validation_metrics={
                'r_squared_adj': float(model.rsquared_adj),
                'aic': float(model.aic),
                'bic': float(model.bic),
                'f_statistic': float(model.fvalue),
                'f_pvalue': float(model.f_pvalue)
            },
            feature_importance=feature_importance,
            last_trained_at=datetime.now(),
        )
    