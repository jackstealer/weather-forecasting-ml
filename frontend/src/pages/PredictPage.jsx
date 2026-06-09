import React, { useState, useEffect } from 'react';
import { 
  MapPin, Droplets, Wind, Gauge, Compass, Calendar, Clock, 
  Loader2, Cloud, TrendingUp, Zap, RefreshCw, Info, HelpCircle
} from 'lucide-react';
import { weatherAPI } from '../services/api';
import WeatherCard from '../components/WeatherCard';
import PredictionGauge from '../components/PredictionGauge';
import MetricCard from '../components/MetricCard';

function PredictPage() {
  const [mode, setMode] = useState('realtime'); // Default to simplest mode
  const [loading, setLoading] = useState(false);
  const [cities, setCities] = useState([]);
  const [weatherData, setWeatherData] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Get current date/time
  const now = new Date();
  
  const [formData, setFormData] = useState({
    city: 'New York, USA',
    latitude: 40.7128,
    longitude: -74.0060,
    humidity: 65,
    pressure: 1013,
    wind_speed: 5.0,
    wind_direction: 180,
    hour: now.getHours(),
    month: now.getMonth() + 1,
    day_of_year: Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 86400000),
    day_of_week: now.getDay(),
  });

  useEffect(() => {
    loadCities();
  }, []);

  const loadCities = async () => {
    try {
      const data = await weatherAPI.getCities();
      setCities(data.cities);
    } catch (error) {
      console.error('Failed to load cities:', error);
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

  const fetchRealtimeWeather = async () => {
    setLoading(true);
    try {
      const data = await weatherAPI.getWeatherByCity(formData.city);
      setWeatherData(data.weather);
      
      // Update form with real-time data
      setFormData(prev => ({
        ...prev,
        latitude: data.weather.latitude,
        longitude: data.weather.longitude,
        humidity: data.weather.humidity,
        pressure: data.weather.pressure,
        wind_speed: data.weather.wind_speed,
        wind_direction: data.weather.wind_direction,
      }));
      
      // Auto-predict after fetching weather
      setTimeout(() => makePrediction(), 500);
    } catch (error) {
      alert('Failed to fetch weather data: ' + (error.error || error.message));
      setLoading(false);
    }
  };

  const makePrediction = async () => {
    setLoading(true);
    try {
      const data = await weatherAPI.predict(formData);
      setPredictions(data.predictions);
    } catch (error) {
      alert('Prediction failed: ' + (error.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: parseFloat(value) || value }));
  };

  return (
    <div className="space-y-6">
      {/* Simple Header with Instructions */}
      <div className="glass-card p-6 text-center">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent mb-3">
          🌡️ Get Weather Predictions
        </h2>
        <p className="text-gray-600 text-lg mb-4">
          Choose your city and get AI-powered temperature predictions instantly!
        </p>
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-50 rounded-lg text-sm text-blue-700">
          <Info className="w-4 h-4" />
          <span>Just select a city and click the button below - it's that simple!</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Simplified Input Panel */}
        <div className="lg:col-span-1 space-y-6">
          {/* City Selection - Prominent */}
          <div className="glass-card p-6 space-y-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xl font-bold text-gray-800 flex items-center">
                <MapPin className="w-5 h-5 mr-2 text-blue-500" />
                Choose Your City
              </h3>
            </div>
            
            <div className="space-y-3">
              <select
                value={formData.city}
                onChange={(e) => handleCityChange(e.target.value)}
                className="input-field text-lg font-medium"
              >
                {cities.map(city => (
                  <option key={city.name} value={city.name}>{city.name}</option>
                ))}
              </select>
              
              <div className="text-xs text-gray-500 bg-gray-50 p-3 rounded-lg">
                <strong>Location:</strong> {formData.latitude.toFixed(2)}°N, {Math.abs(formData.longitude).toFixed(2)}°{formData.longitude < 0 ? 'W' : 'E'}
              </div>
            </div>

            {/* Big Get Weather Button */}
            <button
              onClick={mode === 'realtime' ? fetchRealtimeWeather : makePrediction}
              disabled={loading}
              className="btn-primary w-full text-lg py-4 shadow-2xl"
            >
              {loading ? (
                <>
                  <Loader2 className="inline w-5 h-5 mr-2 animate-spin" />
                  {mode === 'realtime' ? 'Getting Weather...' : 'Predicting...'}
                </>
              ) : mode === 'realtime' ? (
                <>
                  <RefreshCw className="inline w-5 h-5 mr-2" />
                  Get Live Weather & Predict
                </>
              ) : (
                <>
                  <Zap className="inline w-5 h-5 mr-2" />
                  Make Prediction
                </>
              )}
            </button>
          </div>

          {/* Mode Toggle - Simplified */}
          <div className="glass-card p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-semibold text-gray-700">Data Source</span>
              <button
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="text-xs text-blue-600 hover:text-blue-700 flex items-center"
              >
                <HelpCircle className="w-3 h-3 mr-1" />
                {showAdvanced ? 'Hide' : 'Show'} Options
              </button>
            </div>
            
            <div className="space-y-2">
              <button
                onClick={() => setMode('realtime')}
                className={`w-full px-4 py-3 rounded-lg font-medium transition-all ${
                  mode === 'realtime'
                    ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg'
                    : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
                }`}
              >
                <RefreshCw className="inline w-4 h-4 mr-2" />
                Live Weather (Recommended)
              </button>
              
              {showAdvanced && (
                <>
                  <button
                    onClick={() => setMode('city')}
                    className={`w-full px-4 py-3 rounded-lg font-medium transition-all ${
                      mode === 'city'
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg'
                        : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
                    }`}
                  >
                    <MapPin className="inline w-4 h-4 mr-2" />
                    Manual Entry
                  </button>
                  <button
                    onClick={() => setMode('coordinates')}
                    className={`w-full px-4 py-3 rounded-lg font-medium transition-all ${
                      mode === 'coordinates'
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg'
                        : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
                    }`}
                  >
                    <Compass className="inline w-4 h-4 mr-2" />
                    Custom Coordinates
                  </button>
                </>
              )}
            </div>
            
            <div className="mt-3 text-xs text-gray-500 bg-blue-50 p-2 rounded">
              {mode === 'realtime' ? (
                '✓ Fetches current weather data automatically'
              ) : mode === 'city' ? (
                'Enter weather conditions manually'
              ) : (
                'Advanced: Enter exact GPS coordinates'
              )}
            </div>
          </div>

          {/* Advanced Settings - Collapsible */}
          {showAdvanced && mode !== 'realtime' && (
            <>
              {/* Coordinates Input (only for coordinates mode) */}
              {mode === 'coordinates' && (
                <div className="glass-card p-4 space-y-3">
                  <h4 className="text-sm font-semibold text-gray-700">GPS Coordinates</h4>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Latitude</label>
                      <input
                        type="number"
                        step="0.0001"
                        value={formData.latitude}
                        onChange={(e) => handleInputChange('latitude', e.target.value)}
                        className="input-field text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Longitude</label>
                      <input
                        type="number"
                        step="0.0001"
                        value={formData.longitude}
                        onChange={(e) => handleInputChange('longitude', e.target.value)}
                        className="input-field text-sm"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Weather Conditions - Simplified with Sliders */}
              <div className="glass-card p-4 space-y-3">
                <h4 className="text-sm font-semibold text-gray-700 flex items-center">
                  <Cloud className="w-4 h-4 mr-2 text-blue-500" />
                  Weather Conditions
                </h4>
                
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs text-gray-600 mb-1 flex items-center">
                      <Droplets className="w-3 h-3 mr-1" />
                      Humidity (%)
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={formData.humidity}
                      onChange={(e) => handleInputChange('humidity', e.target.value)}
                      className="w-full"
                    />
                    <div className="text-center text-sm font-semibold text-blue-600">{formData.humidity}%</div>
                  </div>
                  
                  <div>
                    <label className="block text-xs text-gray-600 mb-1 flex items-center">
                      <Gauge className="w-3 h-3 mr-1" />
                      Pressure (hPa)
                    </label>
                    <input
                      type="range"
                      min="950"
                      max="1050"
                      value={formData.pressure}
                      onChange={(e) => handleInputChange('pressure', e.target.value)}
                      className="w-full"
                    />
                    <div className="text-center text-sm font-semibold text-blue-600">{formData.pressure} hPa</div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2 space-y-6">
          {weatherData && mode === 'realtime' && (
            <WeatherCard weather={weatherData} />
          )}

          {predictions ? (
            <>
              {/* Model Predictions */}
              <div className="glass-card p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-2 text-center">
                  🌡️ AI Temperature Predictions
                </h3>
                <p className="text-gray-600 text-center mb-6">
                  Results from multiple AI models
                </p>
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  <MetricCard
                    title="Linear Model"
                    value={predictions['Linear Regression']}
                    icon={TrendingUp}
                    color="red"
                  />
                  <MetricCard
                    title="Random Forest"
                    value={predictions['Random Forest']}
                    icon={TrendingUp}
                    color="blue"
                  />
                  <MetricCard
                    title="XGBoost"
                    value={predictions['XGBoost']}
                    icon={TrendingUp}
                    color="green"
                  />
                  <MetricCard
                    title="Best Prediction"
                    value={predictions['Ensemble']}
                    icon={Zap}
                    color="purple"
                  />
                </div>
              </div>

              {/* Gauge Visualization */}
              <div className="glass-card p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-2 text-center">
                  📊 Temperature Reading
                </h3>
                <p className="text-gray-600 text-center mb-6">
                  Our best AI prediction based on all models
                </p>
                <PredictionGauge 
                  value={predictions['Ensemble']} 
                  actual={weatherData?.temperature}
                />
              </div>
            </>
          ) : (
            <div className="glass-card p-12 text-center">
              <div className="space-y-6">
                <div className="inline-block p-8 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full">
                  <Cloud className="w-20 h-20 text-blue-500 animate-float" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-800 mb-3">
                    Ready to Predict!
                  </h3>
                  <p className="text-gray-600 max-w-md mx-auto text-lg leading-relaxed">
                    Select your city from the dropdown and click the big blue button to get instant weather predictions
                  </p>
                </div>
                
                {/* Quick Guide */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl max-w-lg mx-auto text-left">
                  <h4 className="font-bold text-gray-800 mb-3">Quick Guide:</h4>
                  <ol className="space-y-2 text-sm text-gray-700">
                    <li className="flex items-start">
                      <span className="font-bold text-blue-600 mr-2">1.</span>
                      <span>Choose your city from the dropdown menu</span>
                    </li>
                    <li className="flex items-start">
                      <span className="font-bold text-blue-600 mr-2">2.</span>
                      <span>Click "Get Live Weather & Predict"</span>
                    </li>
                    <li className="flex items-start">
                      <span className="font-bold text-blue-600 mr-2">3.</span>
                      <span>See AI predictions from 4 different models!</span>
                    </li>
                  </ol>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PredictPage;
