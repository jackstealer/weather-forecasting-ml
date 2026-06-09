import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Award, Loader2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { weatherAPI } from '../services/api';
import MetricCard from '../components/MetricCard';

function ComparePage() {
  const [loading, setLoading] = useState(false);
  const [modelInfo, setModelInfo] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [cities, setCities] = useState([]);
  
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
  });

  useEffect(() => {
    loadModelInfo();
    loadCities();
  }, []);

  const loadModelInfo = async () => {
    try {
      const data = await weatherAPI.getModelInfo();
      setModelInfo(data);
    } catch (error) {
      console.error('Failed to load model info:', error);
    }
  };

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

  const compareModels = async () => {
    setLoading(true);
    try {
      const data = await weatherAPI.predict(formData);
      setPredictions(data.predictions);
    } catch (error) {
      alert('Comparison failed: ' + (error.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: parseFloat(value) || value }));
  };

  const performanceData = modelInfo?.performance ? 
    Object.entries(modelInfo.performance).map(([name, metrics]) => ({
      name: name.replace(' Regression', '').replace(' ', '\n'),
      MAE: metrics.MAE,
      RMSE: metrics.RMSE,
      'R²': metrics.R2,
    })) : [];

  const predictionData = predictions ?
    Object.entries(predictions).map(([name, temp]) => ({
      name: name.replace(' Regression', '').replace(' ', '\n'),
      temperature: temp,
    })) : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Model Comparison
        </h2>
        <p className="text-gray-600 text-lg">
          Compare performance metrics and predictions across all models
        </p>
      </div>

      {/* Model Performance Overview */}
      {modelInfo && (
        <div className="glass-card p-6">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <Award className="w-6 h-6 mr-2 text-yellow-500" />
            Model Performance (Test Set)
          </h3>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* R² Score Chart */}
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-4">
                R² Score (Higher is Better)
              </h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#6b7280" />
                  <YAxis domain={[0, 1]} stroke="#6b7280" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                      border: '1px solid #e5e7eb',
                      borderRadius: '0.75rem'
                    }}
                    formatter={(value) => value.toFixed(4)}
                  />
                  <Bar dataKey="R²" fill="url(#colorR2)" radius={[8, 8, 0, 0]} />
                  <defs>
                    <linearGradient id="colorR2" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.9}/>
                      <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.6}/>
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* MAE Chart */}
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-4">
                Mean Absolute Error (Lower is Better)
              </h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                      border: '1px solid #e5e7eb',
                      borderRadius: '0.75rem'
                    }}
                    formatter={(value) => `${value.toFixed(3)}°C`}
                  />
                  <Bar dataKey="MAE" fill="url(#colorMAE)" radius={[8, 8, 0, 0]} />
                  <defs>
                    <linearGradient id="colorMAE" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.9}/>
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0.6}/>
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Performance Table */}
          <div className="mt-6 overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b-2 border-gray-200">
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Model</th>
                  <th className="px-4 py-3 text-center font-semibold text-gray-700">R² Score</th>
                  <th className="px-4 py-3 text-center font-semibold text-gray-700">MAE (°C)</th>
                  <th className="px-4 py-3 text-center font-semibold text-gray-700">RMSE (°C)</th>
                </tr>
              </thead>
              <tbody>
                {performanceData.map((model, idx) => (
                  <tr key={idx} className="border-b border-gray-100 hover:bg-blue-50/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-gray-800">{model.name}</td>
                    <td className="px-4 py-3 text-center">
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold">
                        {model['R²'].toFixed(4)}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center text-gray-700">{model.MAE.toFixed(3)}</td>
                    <td className="px-4 py-3 text-center text-gray-700">{model.RMSE.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Live Comparison Section */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Control Panel */}
        <div className="lg:col-span-1 space-y-6">
          <div className="glass-card p-6 space-y-4">
            <h3 className="text-xl font-bold text-gray-800">Make a Prediction</h3>
            
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

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Hour</label>
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
            </div>

            <button
              onClick={compareModels}
              disabled={loading}
              className="btn-primary w-full"
            >
              {loading ? (
                <>
                  <Loader2 className="inline w-4 h-4 mr-2 animate-spin" />
                  Comparing...
                </>
              ) : (
                <>
                  <BarChart3 className="inline w-4 h-4 mr-2" />
                  Compare All Models
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-3 space-y-6">
          {predictions ? (
            <>
              {/* Prediction Cards */}
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard
                  title="Linear Regression"
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
                  title="Ensemble"
                  value={predictions['Ensemble']}
                  icon={Award}
                  color="purple"
                />
              </div>

              {/* Prediction Comparison Chart */}
              <div className="glass-card p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-6">
                  Prediction Comparison
                </h3>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={predictionData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="name" stroke="#6b7280" />
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
                      formatter={(value) => [`${value.toFixed(2)}°C`, 'Temperature']}
                    />
                    <Bar dataKey="temperature" radius={[8, 8, 0, 0]}>
                      {predictionData.map((entry, index) => {
                        const colors = ['#ef4444', '#3b82f6', '#10b981', '#8b5cf6'];
                        return <Bar key={index} dataKey="temperature" fill={colors[index]} />;
                      })}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Statistics */}
              <div className="glass-card p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4">Prediction Statistics</h3>
                <div className="grid grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-sm text-gray-600 mb-2">Mean Prediction</div>
                    <div className="text-3xl font-bold text-blue-600">
                      {(Object.values(predictions).reduce((a, b) => a + b, 0) / 4).toFixed(2)}°C
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-600 mb-2">Standard Deviation</div>
                    <div className="text-3xl font-bold text-purple-600">
                      {Math.sqrt(
                        Object.values(predictions).reduce((sum, val) => {
                          const mean = Object.values(predictions).reduce((a, b) => a + b, 0) / 4;
                          return sum + Math.pow(val - mean, 2);
                        }, 0) / 4
                      ).toFixed(2)}°C
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-600 mb-2">Model Spread</div>
                    <div className="text-3xl font-bold text-orange-600">
                      {(Math.max(...Object.values(predictions)) - Math.min(...Object.values(predictions))).toFixed(2)}°C
                    </div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="glass-card p-12 text-center">
              <div className="space-y-4">
                <div className="inline-block p-6 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full">
                  <BarChart3 className="w-16 h-16 text-blue-500 animate-float" />
                </div>
                <h3 className="text-2xl font-bold text-gray-800">
                  Ready to Compare
                </h3>
                <p className="text-gray-600 max-w-md mx-auto">
                  Configure your parameters and click "Compare All Models" to see 
                  side-by-side predictions from Linear Regression, Random Forest, XGBoost, and Ensemble.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ComparePage;
