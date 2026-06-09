"""
Data processing utilities for combining and preparing weather data
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
from config.config import (
    BASE_DIR, CSV_FILES, COMBINED_DATA_FILE, PROCESSED_DATA_FILE,
    KELVIN_TO_CELSIUS_OFFSET, TEMPERATURE_RANGE, HUMIDITY_RANGE,
    PRESSURE_RANGE, WIND_SPEED_RANGE
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

class WeatherDataProcessor:
    """Processes and combines weather data from multiple CSV files"""
    
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.cities: list = []
    
    def load_csv_files(self, sample_size: Optional[int] = None) -> bool:
        """
        Load and combine all CSV files into a single dataset
        
        Args:
            sample_size: Optional number of rows to sample from each file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Loading CSV files...")
            
            # Load temperature data
            temp_df = pd.read_csv(BASE_DIR / CSV_FILES["temperature"], nrows=sample_size)
            humidity_df = pd.read_csv(BASE_DIR / CSV_FILES["humidity"], nrows=sample_size)
            pressure_df = pd.read_csv(BASE_DIR / CSV_FILES["pressure"], nrows=sample_size)
            wspeed_df = pd.read_csv(BASE_DIR / CSV_FILES["wind_speed"], nrows=sample_size)
            wdir_df = pd.read_csv(BASE_DIR / CSV_FILES["wind_direction"], nrows=sample_size)
            city_attrs = pd.read_csv(BASE_DIR / CSV_FILES["city_attributes"])
            
            # Normalize city attributes column names
            city_attrs.columns = [c.lower() for c in city_attrs.columns]
            
            # Get list of cities (all columns except datetime)
            self.cities = [c for c in temp_df.columns if c != "datetime"]
            logger.info(f"Found {len(self.cities)} cities in dataset")
            
            # Combine data for each city
            frames = []
            for city in self.cities:
                # Check if city exists in all dataframes
                required = [temp_df, humidity_df, pressure_df, wspeed_df, wdir_df]
                if any(city not in df.columns for df in required):
                    logger.warning(f"Skipping city {city} - missing in some data files")
                    continue
                
                city_df = pd.DataFrame({
                    "datetime": pd.to_datetime(temp_df["datetime"]),
                    "city": city,
                    "temperature": temp_df[city],
                    "humidity": humidity_df[city],
                    "pressure": pressure_df[city],
                    "wind_speed": wspeed_df[city],
                    "wind_direction": wdir_df[city],
                })
                
                # Add city coordinates
                city_info = city_attrs[city_attrs["city"] == city]
                if not city_info.empty:
                    city_df["latitude"] = city_info["latitude"].values[0]
                    city_df["longitude"] = city_info["longitude"].values[0]
                    city_df["country"] = city_info["country"].values[0] if "country" in city_info.columns else "Unknown"
                else:
                    logger.warning(f"No coordinates found for {city}, using defaults")
                    city_df["latitude"] = 0.0
                    city_df["longitude"] = 0.0
                    city_df["country"] = "Unknown"
                
                frames.append(city_df)
            
            if not frames:
                logger.error("No city data could be loaded")
                return False
            
            # Combine all city data
            self.data = pd.concat(frames, ignore_index=True)
            logger.info(f"Combined dataset shape: {self.data.shape}")
            
            # Save combined raw data
            self.data.to_csv(COMBINED_DATA_FILE, index=False)
            logger.info(f"Saved combined data to {COMBINED_DATA_FILE}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading CSV files: {e}")
            return False
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and validate the combined dataset
        
        Returns:
            Cleaned DataFrame
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_csv_files() first.")
        
        logger.info("Cleaning data...")
        initial_rows = len(self.data)
        
        # Remove missing values
        self.data = self.data.dropna()
        logger.info(f"Removed {initial_rows - len(self.data)} rows with missing values")
        
        # Convert temperature from Kelvin to Celsius
        self.data["temperature"] = self.data["temperature"] - KELVIN_TO_CELSIUS_OFFSET
        
        # Filter outliers
        self.data = self.data[
            self.data["temperature"].between(*TEMPERATURE_RANGE) &
            self.data["humidity"].between(*HUMIDITY_RANGE) &
            self.data["pressure"].between(*PRESSURE_RANGE) &
            self.data["wind_speed"].between(*WIND_SPEED_RANGE)
        ]
        
        logger.info(f"After cleaning: {len(self.data)} rows remaining")
        
        return self.data
    
    def add_time_features(self) -> pd.DataFrame:
        """
        Add time-based features to the dataset
        
        Returns:
            DataFrame with added time features
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_csv_files() first.")
        
        logger.info("Adding time features...")
        
        self.data = self.data.sort_values("datetime").reset_index(drop=True)
        self.data["hour"] = self.data["datetime"].dt.hour
        self.data["month"] = self.data["datetime"].dt.month
        self.data["day_of_year"] = self.data["datetime"].dt.dayofyear
        self.data["day_of_week"] = self.data["datetime"].dt.dayofweek
        self.data["year"] = self.data["datetime"].dt.year
        
        return self.data
    
    def save_processed_data(self) -> None:
        """Save the processed dataset"""
        if self.data is None:
            raise ValueError("No data to save")
        
        # Save both processed and combined version
        self.data.to_csv(PROCESSED_DATA_FILE, index=False)
        logger.info(f"Saved processed data to {PROCESSED_DATA_FILE}")
        
        # Also save as main combined file
        combined_file = BASE_DIR / "weather_data_combined.csv"
        self.data.to_csv(combined_file, index=False)
        logger.info(f"Saved combined data to {combined_file}")
    
    def process_all(self, sample_size: Optional[int] = None) -> Tuple[pd.DataFrame, list]:
        """
        Execute complete data processing pipeline
        
        Args:
            sample_size: Optional number of rows to sample
        
        Returns:
            Tuple of (processed DataFrame, list of cities)
        """
        logger.info("=" * 70)
        logger.info("Starting data processing pipeline")
        logger.info("=" * 70)
        
        # Load data
        if not self.load_csv_files(sample_size):
            raise RuntimeError("Failed to load CSV files")
        
        # Clean data
        self.clean_data()
        
        # Add time features
        self.add_time_features()
        
        # Save processed data
        self.save_processed_data()
        
        logger.info("=" * 70)
        logger.info("Data processing complete!")
        logger.info(f"Final dataset: {self.data.shape}")
        logger.info(f"Cities: {len(self.cities)}")
        logger.info("=" * 70)
        
        return self.data, self.cities

def load_processed_data() -> Optional[pd.DataFrame]:
    """
    Load previously processed data if available
    
    Returns:
        DataFrame if file exists, None otherwise
    """
    if PROCESSED_DATA_FILE.exists():
        logger.info(f"Loading processed data from {PROCESSED_DATA_FILE}")
        return pd.read_csv(PROCESSED_DATA_FILE, parse_dates=["datetime"])
    return None
