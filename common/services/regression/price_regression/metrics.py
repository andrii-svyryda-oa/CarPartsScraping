from pathlib import Path
import uuid
from common.settings import settings
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
import os
from datetime import datetime

from common.database.models.regression_model import RegressionModel
from common.services.regression.price_regression.predict import PriceRegressionPredictor, PricePredictionInput

class PriceDependencyGraphicsBuilder:
    def __init__(
        self,
        min_rating: int,
        max_rating: int,
        regression_model: RegressionModel,
        min_search_position: int,
        max_search_position: int,
        manufacturers: List[str],
        platforms: List[str]
    ):
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.regression_model = regression_model
        self.min_search_position = min_search_position
        self.max_search_position = max_search_position
        self.manufacturers = manufacturers
        self.platforms = platforms
        self.predictor = PriceRegressionPredictor(regression_model)
        
        self.output_dir = Path(settings.FILES_DIR) / "price_dependency_graphics" / str(uuid.uuid4())
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _generate_rating_data(self, manufacturer: str, platform: str = "default") -> Tuple[np.ndarray, np.ndarray]:
        rating_values = np.linspace(self.min_rating, self.max_rating, 50)
        predicted_prices = []
        
        avg_search_position = (self.min_search_position + self.max_search_position) // 2
        
        for rating in rating_values:
            input_data = PricePredictionInput(
                platform=platform,
                reviews_count=int(rating),
                search_position=avg_search_position,
                manufacturer=manufacturer
            )
            
            prediction = self.predictor.predict_price(input_data)
            predicted_prices.append(prediction.predicted_value)
        
        return rating_values, np.array(predicted_prices)
    
    def _generate_search_position_data(self, manufacturer: str, platform: str = "default") -> Tuple[np.ndarray, np.ndarray]:
        search_position_values = np.linspace(self.min_search_position, self.max_search_position, 50)
        predicted_prices = []
        
        avg_rating = (self.min_rating + self.max_rating) // 2
        
        for search_pos in search_position_values:
            input_data = PricePredictionInput(
                platform=platform,
                reviews_count=avg_rating,
                search_position=int(search_pos),
                manufacturer=manufacturer
            )
            
            prediction = self.predictor.predict_price(input_data)
            predicted_prices.append(prediction.predicted_value)
        
        return search_position_values, np.array(predicted_prices)
    
    def generate_rating_dependency_graphics(self) -> Dict[str, Dict[str, str]]:
        all_results = {}
        
        for platform in self.platforms:
            file_paths = {}
            
            # Create platform-specific subplot figure
            plt.figure(figsize=(15, 10))
            
            for i, manufacturer in enumerate(self.manufacturers):
                try:
                    rating_values, predicted_prices = self._generate_rating_data(manufacturer, platform)
                    
                    # Add to combined plot
                    plt.subplot(2, 2, (i % 4) + 1)
                    plt.plot(rating_values, predicted_prices, linewidth=2, label=f'{manufacturer}')
                    plt.xlabel('Rating (Reviews Count)')
                    plt.ylabel('Predicted Price')
                    plt.title(f'Price vs Rating - {manufacturer} ({platform})')
                    plt.grid(True, alpha=0.3)
                    plt.legend()
                    
                    # Save individual manufacturer-platform graphic
                    individual_filename = f"{self.output_dir}/rating_dependency_{platform}_{manufacturer.replace(' ', '_')}.png"
                    plt.figure(figsize=(10, 6))
                    plt.plot(rating_values, predicted_prices, linewidth=2, color='blue')
                    plt.xlabel('Rating (Reviews Count)')
                    plt.ylabel('Predicted Price')
                    plt.title(f'Price Dependency on Rating - {manufacturer} ({platform})')
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    plt.savefig(individual_filename, dpi=300, bbox_inches='tight')
                    plt.close()
                    
                    file_paths[manufacturer] = individual_filename
                    
                except Exception as e:
                    print(f"Error generating rating dependency for {manufacturer} on {platform}: {str(e)}")
                    continue
            
            # Save combined graphic for platform
            combined_filename = f"{self.output_dir}/rating_dependency_combined_{platform}.png"
            plt.tight_layout()
            plt.savefig(combined_filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            file_paths["combined"] = combined_filename
            all_results[platform] = file_paths
            
        # Generate cross-platform comparison
        self._generate_cross_platform_rating_comparison()
        
        return all_results
    
    def generate_search_position_dependency_graphics(self) -> Dict[str, Dict[str, str]]:
        all_results = {}
        
        for platform in self.platforms:
            file_paths = {}
            
            # Create platform-specific subplot figure
            plt.figure(figsize=(15, 10))
            
            for i, manufacturer in enumerate(self.manufacturers):
                try:
                    search_pos_values, predicted_prices = self._generate_search_position_data(manufacturer, platform)
                    
                    # Add to combined plot
                    plt.subplot(2, 2, (i % 4) + 1)
                    plt.plot(search_pos_values, predicted_prices, linewidth=2, label=f'{manufacturer}')
                    plt.xlabel('Search Position')
                    plt.ylabel('Predicted Price')
                    plt.title(f'Price vs Search Position - {manufacturer} ({platform})')
                    plt.grid(True, alpha=0.3)
                    plt.legend()
                    
                    # Save individual manufacturer-platform graphic
                    individual_filename = f"{self.output_dir}/search_position_dependency_{platform}_{manufacturer.replace(' ', '_')}.png"
                    plt.figure(figsize=(10, 6))
                    plt.plot(search_pos_values, predicted_prices, linewidth=2, color='red')
                    plt.xlabel('Search Position')
                    plt.ylabel('Predicted Price')
                    plt.title(f'Price Dependency on Search Position - {manufacturer} ({platform})')
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    plt.savefig(individual_filename, dpi=300, bbox_inches='tight')
                    plt.close()
                    
                    file_paths[manufacturer] = individual_filename
                    
                except Exception as e:
                    print(f"Error generating search position dependency for {manufacturer} on {platform}: {str(e)}")
                    continue
            
            # Save combined graphic for platform
            combined_filename = f"{self.output_dir}/search_position_dependency_combined_{platform}.png"
            plt.tight_layout()
            plt.savefig(combined_filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            file_paths["combined"] = combined_filename
            all_results[platform] = file_paths
            
        self._generate_cross_platform_search_position_comparison()
        
        return all_results
    
    def generate_all_graphics(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        results = {
            "rating": self.generate_rating_dependency_graphics(),
            "search_position": self.generate_search_position_dependency_graphics()
        }
        
        return results
    
    def _generate_cross_platform_rating_comparison(self) -> None:
        """Generate cross-platform comparison charts for rating dependency."""
        for manufacturer in self.manufacturers:
            plt.figure(figsize=(12, 8))
            
            for platform in self.platforms:
                try:
                    rating_values, predicted_prices = self._generate_rating_data(manufacturer, platform)
                    plt.plot(rating_values, predicted_prices, linewidth=2, label=f'{platform}', marker='o', markersize=4)
                except Exception as e:
                    print(f"Error in cross-platform rating comparison for {manufacturer} on {platform}: {str(e)}")
                    continue
            
            plt.xlabel('Rating (Reviews Count)')
            plt.ylabel('Predicted Price')
            plt.title(f'Cross-Platform Price vs Rating Comparison - {manufacturer}')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            comparison_filename = f"{self.output_dir}/cross_platform_rating_comparison_{manufacturer.replace(' ', '_')}.png"
            plt.savefig(comparison_filename, dpi=300, bbox_inches='tight')
            plt.close()
    
    def _generate_cross_platform_search_position_comparison(self) -> None:
        """Generate cross-platform comparison charts for search position dependency."""
        for manufacturer in self.manufacturers:
            plt.figure(figsize=(12, 8))
            
            for platform in self.platforms:
                try:
                    search_pos_values, predicted_prices = self._generate_search_position_data(manufacturer, platform)
                    plt.plot(search_pos_values, predicted_prices, linewidth=2, label=f'{platform}', marker='s', markersize=4)
                except Exception as e:
                    print(f"Error in cross-platform search position comparison for {manufacturer} on {platform}: {str(e)}")
                    continue
            
            plt.xlabel('Search Position')
            plt.ylabel('Predicted Price')
            plt.title(f'Cross-Platform Price vs Search Position Comparison - {manufacturer}')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            comparison_filename = f"{self.output_dir}/cross_platform_search_position_comparison_{manufacturer.replace(' ', '_')}.png"
            plt.savefig(comparison_filename, dpi=300, bbox_inches='tight')
            plt.close()
