import React, { useState, useEffect } from 'react';
import { MapPin, Cloud, Clock, TrendingUp, Loader2, Activity } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { weatherAPI } from '../services/api';

function ForecastPage() {
  const [loading, setLoading] = useState(false);
  const [cities, setCities] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  
  const [formData, setFormData] = useState({
    city: 'Vancouver',
    latitude: 49.2827,
    longitude: -123.1207,
    humidity: 65,
    pressure: 1013,
    wind_speed: 5.0,
    wind_direction: 180,
    hour: new Date().getHours(),
    month: new Date().getMonth() + 1,
    day_of_year: Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 86400000),
    day_of_week: new Date().getDay(),
    hours_ahead: 48,
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

  const generateForecast = async () => {
    setLoading(true);
    try {
      const data = await weatherAPI.forecast(formData);
      setForecastData(data);
    } catch (error) {
      alert('Forecast generation failed: ' + (error.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: parseFloat(value) || value }));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Multi-Hour Forecast
        </h2>
        <p className="text-gray-600 text-lg">
          Generate temperature forecasts up to 7 days ahead
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Control Panel */}
        <div className="lg:col-span-1 space-y-6">
          {/* Location */}
          <div className="glass-card p-6 space-y-4">
            <h3 className="text-xl font-bold text-gray-800 flex items-center">
              <MapPin className="w-5 h-5 mr-2 text-blue-500" />
              Location
            </h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
              <select
                value={formData.city}
                onChange={(e) => handleCityChange(e.target.value)}
                className="input-field"
              >
                {cities.map(city => (
                  <option key={city.name} value={city.name}>{city.name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Weather Parameters */}
          <div className="glass-card p-6 space-y-4">
            <h3 className="text-xl font-bold text-gray-800 flex items-center">
              <Cloud className="w-5 h-5 mr-2 text-blue-500" />
              Weather
            </h3>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Humidity (%)</label>
                <input
                  type="number"
                  value={formData.humidity}
                  onChange={(e) => handleInputChange('humidity', e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Pressure (hPa)</label>
                <input
                  type="number"
                  value={formData.pressure}
                  onChange={(e) => handleInputChange('pressure', e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Wind Speed (m/s)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.wind_speed}
                  onChange={(e) => handleInputChange('wind_speed', e.target.value)}
                  className="input-field"
                />
              </div>
            </div>
          </div>

          {/* Time Settings */}
          <div className="glass-card p-6 space-y-4">
            <h3 className="text-xl font-bold text-gray-800 flex items-center">
              <Clock className="w-5 h-5 mr-2 text-blue-500" />
              Time
            </h3>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Start Hour</label>
                <input
                  type="number"
                  min="0"
                  max="23"
                  value={formData.hour}
                  onChange={(e) => handleInputChange('hour', e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Month</label>
                <input
                  type="number"
                  min="1"
                  max="12"
                  value={formData.month}
                  onChange={(e) => handleInputChange('month', e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Forecast Duration (hours)</label>
                <select
                  value={formData.hours_ahead}
                  onChange={(e) => handleInputChange('hours_ahead', e.target.value)}
                  className="input-field"
                >
                  <option value={12}>12 hours</option>
                  <option value={24}>24 hours (1 day)</option>
                  <option value={48}>48 hours (2 days)</option>
                  <option value={72}>72 hours (3 days)</option>
                  <option value={120}>120 hours (5 days)</option>
                  <option value={168}>168 hours (7 days)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={generateForecast}
            disabled={loading}
            className="btn-primary w-full text-lg py-4"
          >
            {loading ? (
              <>
                <Loader2 className="inline w-5 h-5 mr-2 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Activity className="inline w-5 h-5 mr-2" />
                Generate Forecast
              </>
            )}
          </button>

          {forecastData && (
            <div className="glass-card p-4 space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Duration:</span>
                <span className="font-bold">{forecastData.hours_ahead} hours</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Data Points:</span>
                <span className="font-bold">{forecastData.forecast.length}</span>
              </div>
            </div>
          )}
        </div>

        {/* Visualization Panel */}
        <div className="lg:col-span-3 space-y-6">
          {forecastData ? (
            <>
              {/* Statistics Cards */}
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="glass-card p-6">
                  <div className="text-sm text-gray-600 mb-1">Average</div>
                  <div className="text-3xl font-bold text-blue-600">
                    {forecastData.statistics.mean.toFixed(1)}°C
                  </div>
                </div>
                <div className="glass-card p-6">
                  <div className="text-sm text-gray-600 mb-1">Maximum</div>
                  <div className="text-3xl font-bold text-red-600">
                    {forecastData.statistics.max.toFixed(1)}°C
                  </div>
                </div>
                <div className="glass-card p-6">
                  <div className="text-sm text-gray-600 mb-1">Minimum</div>
                  <div className="text-3xl font-bold text-blue-600">
                    {forecastData.statistics.min.toFixed(1)}°C
                  </div>
                </div>
                <div className="glass-card p-6">
                  <div className="text-sm text-gray-600 mb-1">Range</div>
                  <div className="text-3xl font-bold text-purple-600">
                    {forecastData.statistics.range.toFixed(1)}°C
                  </div>
                </div>
              </div>

              {/* Forecast Chart */}
              <div className="glass-card p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-6">
                  Temperature Forecast
                </h3>
                <ResponsiveContainer width="100%" height={400}>
                  <AreaChart data={forecastData.forecast}>
                    <defs>
                      <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="hours_ahead" 
                      label={{ value: 'Hours Ahead', position: 'insideBottom', offset: -5 }}
                      stroke="#6b7280"
                    />
                    <YAxis 
                      label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }}
                      stroke="#6b7280"
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e5e7eb',
                        borderRadius: '0.75rem',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                      }}
                      formatter={(value) => [`${value.toFixed(1)}°C`, 'Temperature']}
                      labelFormatter={(label) => `${label} hours ahead`}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="temperature" 
                      stroke="#3b82f6" 
                      strokeWidth={3}
                      fill="url(#colorTemp)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              {/* Model Breakdown Chart */}
              <div className="glass-card p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-6">
                  Model Comparison
                </h3>
                <ResponsiveContainer width="100%" height={350}>
                  <LineChart data={forecastData.forecast}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="hours_ahead" 
                      label={{ value: 'Hours Ahead', position: 'insideBottom', offset: -5 }}
                      stroke="#6b7280"
                    />
                    <YAxis 
                      label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }}
                      stroke="#6b7280"
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e5e7eb',
                        borderRadius: '0.75rem',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                      }}
                      formatter={(value) => `${value.toFixed(1)}°C`}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey={(d) => d.all_predictions['Linear Regression']}
                      name="Linear Regression"
                      stroke="#ef4444" 
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line 
                      type="monotone" 
                      dataKey={(d) => d.all_predictions['Random Forest']}
                      name="Random Forest"
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line 
                      type="monotone" 
                      dataKey={(d) => d.all_predictions['XGBoost']}
                      name="XGBoost"
                      stroke="#10b981" 
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line 
                      type="monotone" 
                      dataKey={(d) => d.all_predictions['Ensemble']}
                      name="Ensemble"
                      stroke="#8b5cf6" 
                      strokeWidth={3}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </>
          ) : (
            <div className="glass-card p-12 text-center">
              <div className="space-y-4">
                <div className="inline-block p-6 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full">
                  <Activity className="w-16 h-16 text-blue-500 animate-float" />
                </div>
                <h3 className="text-2xl font-bold text-gray-800">
                  Ready to Forecast
                </h3>
                <p className="text-gray-600 max-w-md mx-auto">
                  Configure your parameters and select the forecast duration to generate 
                  multi-hour temperature predictions with visualizations.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ForecastPage;
