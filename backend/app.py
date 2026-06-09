"""
Flask Backend API for Weather Forecasting Application
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.features import build_features, validate_inputs, FEATURE_COLS
from ml.model_manager import model_manager
from ml.weather_api import weather_api

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load models on startup
@app.before_request
def initialize():
    """Initialize models before first request"""
    if not model_manager.is_loaded():
        success = model_manager.load_models()
        if not success:
            app.logger.error("Failed to load ML models")

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model_manager.is_loaded(),
        'api_available': weather_api.is_available(),
        'timestamp': datetime.now().isoformat()
    })

# Model info endpoint
@app.route('/api/models/info', methods=['GET'])
def get_model_info():
    """Get information about loaded models"""
    if not model_manager.is_loaded():
        return jsonify({'error': 'Models not loaded'}), 503
    
    info = model_manager.get_model_info()
    performance = model_manager.get_model_performance()
    
    return jsonify({
        'models': info['model_names'],
        'num_features': info['num_features'],
        'performance': performance,
        'metadata': info.get('metadata', {})
    })

# Prediction endpoint
@app.route('/api/predict', methods=['POST'])
def predict():
    """Make temperature prediction"""
    try:
        data = request.json
        
        # Extract parameters
        humidity = float(data.get('humidity'))
        pressure = float(data.get('pressure'))
        wind_speed = float(data.get('wind_speed'))
        wind_direction = float(data.get('wind_direction'))
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        hour = int(data.get('hour'))
        month = int(data.get('month'))
        day_of_year = int(data.get('day_of_year'))
        day_of_week = int(data.get('day_of_week'))
        
        # Validate inputs
        errors = validate_inputs(humidity, pressure, wind_speed, wind_direction, latitude, longitude)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Build features
        X = build_features(
            humidity, pressure, wind_speed, wind_direction,
            latitude, longitude, hour, month, day_of_year, day_of_week
        )
        
        # Get predictions
        predictions = model_manager.predict_all(X)
        
        return jsonify({
            'predictions': predictions,
            'input': data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

# Forecast endpoint
@app.route('/api/forecast', methods=['POST'])
def forecast():
    """Generate multi-hour forecast"""
    try:
        data = request.json
        
        # Extract base parameters
        humidity = float(data.get('humidity'))
        pressure = float(data.get('pressure'))
        wind_speed = float(data.get('wind_speed'))
        wind_direction = float(data.get('wind_direction'))
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        hour = int(data.get('hour'))
        month = int(data.get('month'))
        day_of_year = int(data.get('day_of_year'))
        day_of_week = int(data.get('day_of_week'))
        hours_ahead = int(data.get('hours_ahead', 48))
        
        # Validate inputs
        errors = validate_inputs(humidity, pressure, wind_speed, wind_direction, latitude, longitude)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Generate forecast
        forecast_data = []
        for h in range(hours_ahead):
            total_h = hour + h
            fc_hour = total_h % 24
            fc_doy = day_of_year + total_h // 24
            fc_dow = (day_of_week + total_h // 24) % 7
            
            X = build_features(
                humidity, pressure, wind_speed, wind_direction,
                latitude, longitude, fc_hour, month, fc_doy, fc_dow
            )
            
            predictions = model_manager.predict_all(X)
            
            forecast_data.append({
                'hours_ahead': h,
                'hour': fc_hour,
                'day_of_year': fc_doy,
                'temperature': predictions['Ensemble'],
                'all_predictions': predictions
            })
        
        # Calculate statistics
        temps = [item['temperature'] for item in forecast_data]
        stats = {
            'mean': sum(temps) / len(temps),
            'min': min(temps),
            'max': max(temps),
            'range': max(temps) - min(temps)
        }
        
        return jsonify({
            'forecast': forecast_data,
            'statistics': stats,
            'hours_ahead': hours_ahead,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"Forecast error: {e}")
        return jsonify({'error': str(e)}), 500

# Weather API endpoint
@app.route('/api/weather/city/<city>', methods=['GET'])
def get_weather_by_city(city):
    """Fetch real-time weather data by city name"""
    try:
        if not weather_api.is_available():
            return jsonify({'error': 'Weather API not configured'}), 503
        
        weather_data = weather_api.fetch_by_city(city)
        
        if not weather_data:
            return jsonify({'error': f'Could not fetch weather data for {city}'}), 404
        
        # Convert datetime to string
        weather_data['datetime'] = weather_data['datetime'].isoformat()
        
        return jsonify({
            'weather': weather_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"Weather API error: {e}")
        return jsonify({'error': str(e)}), 500

# Weather by coordinates
@app.route('/api/weather/coordinates', methods=['POST'])
def get_weather_by_coordinates():
    """Fetch real-time weather data by coordinates"""
    try:
        data = request.json
        lat = float(data.get('latitude'))
        lon = float(data.get('longitude'))
        
        if not weather_api.is_available():
            return jsonify({'error': 'Weather API not configured'}), 503
        
        weather_data = weather_api.fetch_by_coordinates(lat, lon)
        
        if not weather_data:
            return jsonify({'error': 'Could not fetch weather data'}), 404
        
        # Convert datetime to string
        weather_data['datetime'] = weather_data['datetime'].isoformat()
        
        return jsonify({
            'weather': weather_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"Weather API error: {e}")
        return jsonify({'error': str(e)}), 500

# Default cities endpoint
@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get list of default cities"""
    from ml.config import DEFAULT_CITIES
    
    cities = [
        {'name': name, 'latitude': coords['lat'], 'longitude': coords['lon']}
        for name, coords in DEFAULT_CITIES.items()
    ]
    
    return jsonify({'cities': cities})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("WEATHER FORECASTING API SERVER")
    print("=" * 70)
    print("\n🚀 Starting Flask backend...")
    print("📍 API will be available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /api/health              - Health check")
    print("  GET  /api/models/info         - Model information")
    print("  POST /api/predict             - Make prediction")
    print("  POST /api/forecast            - Generate forecast")
    print("  GET  /api/weather/city/<city> - Get weather by city")
    print("  POST /api/weather/coordinates - Get weather by coordinates")
    print("  GET  /api/cities              - List default cities")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
