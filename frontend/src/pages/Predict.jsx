import React, { useState, useEffect } from 'react';
import { weatherAPI } from '../services/api';
import { MapPin, Thermometer, Droplets, Wind, Gauge, Loader } from 'lucide-react';

const Predict = () => {
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState(null);
  const [cities, setCities] = useState([]);
  const [mode, setMode] = useState('city'); // 'city', 'coordinates', 'api'
  
  const [formData, setFormData] = useState({
    city: '',
    latitude: 40.0,
    longitude: -100.0,
    humidity: 65,
    pressure: 1013,
    wind_speed: 5.0,
    wind_direction: 180,
    hour: new Date().getHours(),
    month: new Date().getMonth() + 1,
    day_of_year: Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 86400000),
    day_of_week: new Date().getDay(),
  });

  useEffect(() => {
    loadCities();
  }, []);

  const loadCities = async () => {
    try {
      const response = await weatherAPI.getCities();
      setCities(response.data.cities);
      if (response.data.cities.length > 0) {
        const firstCity = response.data.cities[0];
        setFormData(prev => ({
          ...prev,
          city: firstCity.name,
          latitude: firstCity.latitude,
          longitude: firstCity.longitude,
        }));
      }
    } catch (error) {
      console.error('Error loading cities:', error);
    }
  };

  const handleCityChange = (cityName) => {
    const city = cities.find(c => c.name === cityName);
    if (city) {
      setFormData(prev => ({
        ...prev,
        city: cityName,
        latitude: city.latitude,
        longitude: city.longitude,
      }));
    }
  };

  const fetchRealTimeWeather = async () => {
    setLoading(true);
    try {
      const response = await weatherAPI.getWeatherByCity(formData.city);
      const weather = response.data.weather;
      
      const now = new Date(weather.datetime);
      setFormData(prev => ({
        ...prev,
        humidity: weather.humidity,
        pressure: weather.pressure,
        wind_speed: weather.wind_speed,
        wind_direction: weather.wind_direction,
        latitude: weather.latitude,
        longitude: weather.longitude,
        hour: now.getHours(),
        month: now.getMonth() + 1,
        day_of_year: Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 86400000),
        day_of_week: now.getDay(),
      }));
    } catch (error) {
      console.error('Error fetching weather:', error);
      alert('Failed to fetch real-time weather data');
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await weatherAPI.predict(formData);
      setPredictions(response.data.predictions);
    } catch (error) {
      console.error('Error making prediction:', error);
      alert('Failed to make prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          Temperature Prediction
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Panel */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Input Parameters</h2>
            
            {/* Mode Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Input Mode
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => setMode('city')}
                  className={`px-4 py-2 rounded-lg font-medium ${
                    mode === 'city'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  City
                </button>
                <button
                  onClick={() => setMode('coordinates')}
                  className={`px-4 py-2 rounded-lg font-medium ${
                    mode === 'coordinates'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Coordinates
                </button>
                <button
                  onClick={() => setMode('api')}
                  className={`px-4 py-2 rounded-lg font-medium ${
                    mode === 'api'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Real-time
                </button>
              </div>
            </div>

            {/* Location Input */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="inline h-4 w-4 mr-1" />
                Location
              </label>
              
              {(mode === 'city' || mode === 'api') && (
                <select
                  value={formData.city}
                  onChange={(e) => handleCityChange(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {cities.map(city => (
                    <option key={city.name} value={city.name}>{city.name}</option>
                  ))}
                </select>
              )}
              
              {mode === 'coordinates' && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs text-gray-600">Latitude</label>
                    <input
                      type="number"
                      value={formData.latitude}
                      onChange={(e) => handleChange('latitude', parseFloat(e.target.value))}
                      step="0.1"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-gray-600">Longitude</label>
                    <input
                      type="number"
                      value={formData.longitude}
                      onChange={(e) => handleChange('longitude', parseFloat(e.target.value))}
                      step="0.1"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                    />
                  </div>
                </div>
              )}
            </div>

            {mode === 'api' && (
              <button
                onClick={fetchRealTimeWeather}
                disabled={loading}
                className="w-full mb-6 px-6 py-3 bg-green-500 text-white rounded-lg font-semibold hover:bg-green-600 disabled:bg-gray-300"
              >
                {loading ? 'Fetching...' : 'Fetch Real-time Weather'}
              </button>
            )}

            {/* Weather Parameters */}
            {mode !== 'api' && (
              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Droplets className="inline h-4 w-4 mr-1" />
                    Humidity: {formData.humidity}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={formData.humidity}
                    onChange={(e) => handleChange('humidity', parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Gauge className="inline h-4 w-4 mr-1" />
                    Pressure: {formData.pressure} hPa
                  </label>
                  <input
                    type="range"
                    min="950"
                    max="1050"
                    value={formData.pressure}
                    onChange={(e) => handleChange('pressure', parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Wind className="inline h-4 w-4 mr-1" />
                    Wind Speed: {formData.wind_speed} m/s
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="30"
                    step="0.5"
                    value={formData.wind_speed}
                    onChange={(e) => handleChange('wind_speed', parseFloat(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Wind Direction: {formData.wind_direction}°
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="360"
                    step="10"
                    value={formData.wind_direction}
                    onChange={(e) => handleChange('wind_direction', parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>
              </div>
            )}

            {/* Predict Button */}
            <button
              onClick={handlePredict}
              disabled={loading}
              className="w-full px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-gray-300 flex items-center justify-center"
            >
              {loading ? (
                <><Loader className="animate-spin h-5 w-5 mr-2" /> Processing...</>
              ) : (
                <><Thermometer className="h-5 w-5 mr-2" /> Predict Temperature</>
              )}
            </button>
          </div>

          {/* Results Panel */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Predictions</h2>
            
            {predictions ? (
              <div className="space-y-6">
                {/* Model Predictions */}
                <div className="grid grid-cols-2 gap-4">
                  {Object.entries(predictions).map(([model, temp]) => {
                    const colors = {
                      'Linear Regression': 'from-red-400 to-red-600',
                      'Random Forest': 'from-blue-400 to-blue-600',
                      'XGBoost': 'from-green-400 to-green-600',
                      'Ensemble': 'from-purple-400 to-purple-600',
                    };
                    
                    return (
                      <div
                        key={model}
                        className={`bg-gradient-to-br ${colors[model] || 'from-gray-400 to-gray-600'} rounded-lg p-6 text-white card-hover`}
                      >
                        <h3 className="text-lg font-semibold mb-2">{model}</h3>
                        <div className="text-4xl font-bold">{temp.toFixed(1)}°C</div>
                      </div>
                    );
                  })}
                </div>

                {/* Ensemble Highlight */}
                <div className="bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl p-8 text-white text-center">
                  <h3 className="text-2xl font-bold mb-2">Ensemble Prediction</h3>
                  <div className="text-6xl font-bold mb-2">
                    {predictions.Ensemble?.toFixed(1)}°C
                  </div>
                  <p className="text-purple-100">
                    Weighted average of all models
                  </p>
                </div>

                {/* Statistics */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-2xl font-bold text-gray-900">
                      {Math.max(...Object.values(predictions)).toFixed(1)}°C
                    </div>
                    <div className="text-sm text-gray-600">Maximum</div>
                  </div>
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-2xl font-bold text-gray-900">
                      {Math.min(...Object.values(predictions)).toFixed(1)}°C
                    </div>
                    <div className="text-sm text-gray-600">Minimum</div>
                  </div>
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-2xl font-bold text-gray-900">
                      {(Math.max(...Object.values(predictions)) - Math.min(...Object.values(predictions))).toFixed(1)}°C
                    </div>
                    <div className="text-sm text-gray-600">Range</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <Thermometer className="h-16 w-16 mx-auto mb-4" />
                <p>Enter parameters and click Predict to see results</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Predict;
