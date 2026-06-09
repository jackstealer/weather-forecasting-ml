"""
Configuration management for Weather Forecasting Application
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# API Configuration
OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_TIMEOUT = 10  # seconds

# Model Configuration
MODEL_FILES = {
    "Linear Regression": "linear_regression_model.pkl",
    "Random Forest": "random_forest_model.pkl",
    "XGBoost": "xgboost_model.pkl",
}
SCALER_FILE = "scaler.pkl"
FEATURE_NAMES_FILE = "feature_names.pkl"
METADATA_FILE = "metadata.json"

# Ensemble weights for model predictions
ENSEMBLE_WEIGHTS = {
    "XGBoost": 0.50,
    "Random Forest": 0.35,
    "Linear Regression": 0.15,
}

# Training Configuration
TRAIN_TEST_SPLIT = 0.80  # 80% train, 20% test
RANDOM_STATE = 42
SAMPLE_SIZE = None  # None for full dataset, set integer for subset

# Data Processing Configuration
KELVIN_TO_CELSIUS_OFFSET = 273.15
TEMPERATURE_RANGE = (-50, 60)  # Celsius
HUMIDITY_RANGE = (0, 100)  # Percentage
PRESSURE_RANGE = (900, 1100)  # hPa
WIND_SPEED_RANGE = (0, 50)  # m/s
WIND_DIRECTION_RANGE = (0, 360)  # Degrees

# CSV Data Files
CSV_FILES = {
    "temperature": "temperature.csv",
    "humidity": "humidity.csv",
    "pressure": "pressure.csv",
    "wind_speed": "wind_speed.csv",
    "wind_direction": "wind_direction.csv",
    "weather_description": "weather_description.csv",
    "city_attributes": "city_attributes.csv",
}

# Combined data output
COMBINED_DATA_FILE = DATA_DIR / "combined_weather_data.csv"
PROCESSED_DATA_FILE = DATA_DIR / "processed_weather_data.csv"

# Feature columns - canonical order
FEATURE_COLS = [
    "humidity",
    "pressure",
    "wind_speed",
    "wind_direction",
    "latitude",
    "longitude",
    "hour",
    "month",
    "day_of_year",
    "day_of_week",
    "month_sin",
    "month_cos",
    "hour_sin",
    "hour_cos",
    "day_sin",
    "day_cos",
    "day_of_week_sin",
    "day_of_week_cos",
    "humidity_pressure",
    "wind_speed_squared",
    "dewpoint_approx",
]

# Streamlit App Configuration
APP_TITLE = "Weather Forecasting System"
APP_ICON = "🌤️"
APP_LAYOUT = "wide"
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
    "layout": APP_LAYOUT,
    "initial_sidebar_state": "expanded",
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "weather_app.log"

# Import comprehensive city database
from ml.world_cities import WORLD_CITIES

# Default cities with coordinates - Using comprehensive world database
DEFAULT_CITIES = WORLD_CITIES

def validate_config() -> bool:
    """Validate that all required configurations are set"""
    errors = []
    
    # Check if data directory exists and has CSV files
    if not DATA_DIR.exists():
        errors.append(f"Data directory not found: {DATA_DIR}")
    
    # Check for required CSV files
    for name, filename in CSV_FILES.items():
        filepath = BASE_DIR / filename
        if not filepath.exists():
            errors.append(f"Required CSV file not found: {filename}")
    
    if errors:
        print("Configuration validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

def get_api_status() -> dict:
    """Check API configuration status"""
    return {
        "api_key_configured": bool(OPENWEATHER_API_KEY),
        "api_url": OPENWEATHER_BASE_URL,
        "fallback_mode": not bool(OPENWEATHER_API_KEY),
    }
