"""
Real-time weather API integration using OpenWeatherMap
"""
import requests
from datetime import datetime
from typing import Optional, Dict, Any
from config.config import (
    OPENWEATHER_API_KEY,
    OPENWEATHER_BASE_URL,
    OPENWEATHER_TIMEOUT,
    DEFAULT_CITIES
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

class WeatherAPIClient:
    """Client for fetching real-time weather data from OpenWeatherMap"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Weather API client
        
        Args:
            api_key: OpenWeatherMap API key (uses env variable if not provided)
        """
        self.api_key = api_key or OPENWEATHER_API_KEY
        self.base_url = OPENWEATHER_BASE_URL
        
        if not self.api_key:
            logger.warning("No API key configured. Real-time weather unavailable.")
    
    def is_available(self) -> bool:
        """Check if API is available (key configured)"""
        return bool(self.api_key)
    
    def fetch_by_city(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Fetch weather data for a specific city
        
        Args:
            city: City name
        
        Returns:
            Dictionary with weather data or None if failed
        """
        if not self.api_key:
            logger.error("API key not configured")
            return None
        
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Get Celsius directly
            }
            
            logger.info(f"Fetching weather data for {city}")
            response = requests.get(
                self.base_url,
                params=params,
                timeout=OPENWEATHER_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            return self._parse_response(data)
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                logger.error("Invalid API key")
            elif response.status_code == 404:
                logger.error(f"City not found: {city}")
            else:
                logger.error(f"HTTP error: {e}")
            return None
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def fetch_by_coordinates(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Fetch weather data for specific coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            Dictionary with weather data or None if failed
        """
        if not self.api_key:
            logger.error("API key not configured")
            return None
        
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            logger.info(f"Fetching weather data for coordinates ({lat}, {lon})")
            response = requests.get(
                self.base_url,
                params=params,
                timeout=OPENWEATHER_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            return self._parse_response(data)
            
        except Exception as e:
            logger.error(f"Error fetching data by coordinates: {e}")
            return None
    
    def _parse_response(self, data: Dict) -> Dict[str, Any]:
        """
        Parse OpenWeatherMap API response into standardized format
        
        Args:
            data: Raw API response
        
        Returns:
            Parsed weather data dictionary
        """
        try:
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "datetime": datetime.fromtimestamp(data["dt"]),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", 0),
                "latitude": data["coord"]["lat"],
                "longitude": data["coord"]["lon"],
                "weather_description": data["weather"][0]["description"],
                "weather_main": data["weather"][0]["main"],
                "feels_like": data["main"]["feels_like"],
                "temp_min": data["main"]["temp_min"],
                "temp_max": data["main"]["temp_max"],
                "visibility": data.get("visibility", 10000),
                "clouds": data.get("clouds", {}).get("all", 0),
            }
        except KeyError as e:
            logger.error(f"Error parsing API response: missing key {e}")
            raise
    
    def get_mock_data(self, city: str = "New York") -> Dict[str, Any]:
        """
        Generate mock weather data when API is unavailable
        
        Args:
            city: City name for mock data
        
        Returns:
            Mock weather data dictionary
        """
        coords = DEFAULT_CITIES.get(city, {"lat": 40.7128, "lon": -74.0060})
        
        return {
            "city": city,
            "country": "Mock",
            "datetime": datetime.now(),
            "temperature": 20.0,
            "humidity": 65,
            "pressure": 1013,
            "wind_speed": 5.0,
            "wind_direction": 180,
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "weather_description": "clear sky",
            "weather_main": "Clear",
            "feels_like": 19.0,
            "temp_min": 18.0,
            "temp_max": 22.0,
            "visibility": 10000,
            "clouds": 0,
        }
    
    def test_connection(self) -> bool:
        """
        Test API connection
        
        Returns:
            True if API is working, False otherwise
        """
        if not self.is_available():
            logger.warning("API key not configured")
            return False
        
        try:
            result = self.fetch_by_city("London")
            if result:
                logger.info("API connection test successful")
                return True
            else:
                logger.error("API connection test failed")
                return False
        except Exception as e:
            logger.error(f"API connection test error: {e}")
            return False

# Global instance
weather_api = WeatherAPIClient()
