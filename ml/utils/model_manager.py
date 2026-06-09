"""
Model management utilities for loading and using trained ML models
Supports both traditional ML models and Deep Learning models
"""
import joblib
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from config.config import (
    MODELS_DIR, MODEL_FILES, SCALER_FILE, FEATURE_NAMES_FILE,
    METADATA_FILE, ENSEMBLE_WEIGHTS
)
from utils.logger import setup_logger

# Try importing TensorFlow for deep learning support
try:
    import tensorflow as tf
    from tensorflow import keras
    DL_AVAILABLE = True
except ImportError:
    DL_AVAILABLE = False

logger = setup_logger(__name__)

class ModelManager:
    """Manages ML models for weather prediction"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.dl_model: Optional[Any] = None
        self.dl_scaler: Optional[Any] = None
        self.scaler: Optional[Any] = None
        self.feature_names: list = []
        self.metadata: Dict = {}
        self.dl_metadata: Dict = {}
        self.loaded: bool = False
        self.dl_loaded: bool = False
    
    def load_models(self) -> bool:
        """
        Load all trained models from disk (ML + DL)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Loading ML models...")
            
            # Check if models directory exists
            if not MODELS_DIR.exists():
                logger.error(f"Models directory not found: {MODELS_DIR}")
                return False
            
            # Load each traditional ML model
            for model_name, filename in MODEL_FILES.items():
                model_path = MODELS_DIR / filename
                if not model_path.exists():
                    logger.error(f"Model file not found: {model_path}")
                    return False
                
                self.models[model_name] = joblib.load(model_path)
                logger.info(f"Loaded {model_name}")
            
            # Load scaler
            scaler_path = MODELS_DIR / SCALER_FILE
            if not scaler_path.exists():
                logger.error(f"Scaler file not found: {scaler_path}")
                return False
            self.scaler = joblib.load(scaler_path)
            logger.info("Loaded scaler")
            
            # Load feature names
            feature_path = MODELS_DIR / FEATURE_NAMES_FILE
            if not feature_path.exists():
                logger.error(f"Feature names file not found: {feature_path}")
                return False
            self.feature_names = joblib.load(feature_path)
            logger.info(f"Loaded {len(self.feature_names)} feature names")
            
            # Load metadata if available
            metadata_path = MODELS_DIR / METADATA_FILE
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                logger.info("Loaded model metadata")
            
            # Try loading deep learning model
            if DL_AVAILABLE:
                dl_model_path = MODELS_DIR / "deep_learning_model.h5"
                if dl_model_path.exists():
                    try:
                        self.dl_model = keras.models.load_model(dl_model_path)
                        logger.info("Loaded Deep Learning model")
                        
                        # Load DL scaler
                        dl_scaler_path = MODELS_DIR / "dl_scaler.pkl"
                        if dl_scaler_path.exists():
                            self.dl_scaler = joblib.load(dl_scaler_path)
                            logger.info("Loaded DL scaler")
                        
                        # Load DL metadata
                        dl_metadata_path = MODELS_DIR / "dl_metadata.json"
                        if dl_metadata_path.exists():
                            with open(dl_metadata_path, 'r') as f:
                                self.dl_metadata = json.load(f)
                            logger.info("Loaded DL metadata")
                        
                        self.dl_loaded = True
                    except Exception as e:
                        logger.warning(f"Failed to load DL model: {e}")
                        self.dl_loaded = False
            
            self.loaded = True
            total_models = len(self.models) + (1 if self.dl_loaded else 0)
            logger.info(f"Successfully loaded {total_models} models")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.loaded = False
            return False
    
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self.loaded
    
    def predict(self, X: pd.DataFrame, model_name: str = "XGBoost") -> float:
        """
        Make a prediction using a specific model
        
        Args:
            X: Feature DataFrame (single row)
            model_name: Name of the model to use
        
        Returns:
            Predicted temperature in Celsius
        """
        if not self.loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.models[model_name].predict(X_scaled)[0]
        return float(prediction)
    
    def predict_all(self, X: pd.DataFrame) -> Dict[str, float]:
        """
        Make predictions using all models and compute ensemble
        
        Args:
            X: Feature DataFrame (single row)
        
        Returns:
            Dictionary with predictions from each model and ensemble
        """
        if not self.loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        predictions = {}
        
        # Get prediction from each traditional ML model
        for model_name in self.models.keys():
            predictions[model_name] = self.predict(X, model_name)
        
        # Get prediction from deep learning model if available
        if self.dl_loaded and self.dl_model is not None:
            try:
                X_scaled = self.dl_scaler.transform(X)
                dl_pred = self.dl_model.predict(X_scaled, verbose=0).flatten()[0]
                predictions["Deep Learning"] = float(dl_pred)
            except Exception as e:
                logger.warning(f"DL prediction failed: {e}")
        
        # Compute weighted ensemble (prioritize DL if available)
        if "Deep Learning" in predictions:
            # New ensemble with Deep Learning
            ensemble = (
                predictions["Deep Learning"] * 0.40 +  # 40% DL (best)
                predictions.get("XGBoost", 0) * 0.30 +  # 30% XGBoost
                predictions.get("Random Forest", 0) * 0.20 +  # 20% RF
                predictions.get("Linear Regression", 0) * 0.10  # 10% LR
            )
        else:
            # Original ensemble without DL
            ensemble = sum(
                predictions.get(m, 0) * w
                for m, w in ENSEMBLE_WEIGHTS.items()
                if m in predictions
            )
        
        predictions["Ensemble"] = round(ensemble, 2)
        
        return predictions
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about loaded models
        
        Returns:
            Dictionary with model information
        """
        info = {
            "loaded": self.loaded,
            "num_models": len(self.models),
            "model_names": list(self.models.keys()),
            "num_features": len(self.feature_names),
            "feature_names": self.feature_names,
            "metadata": self.metadata,
        }
        return info
    
    def get_model_performance(self) -> Optional[Dict[str, Dict]]:
        """
        Get model performance metrics from metadata
        
        Returns:
            Dictionary with performance metrics for each model
        """
        if not self.metadata or "results" not in self.metadata:
            return None
        
        return self.metadata["results"]

# Global instance
model_manager = ModelManager()
