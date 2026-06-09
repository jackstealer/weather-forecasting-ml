import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { weatherAPI } from '../services/api';
import { Target, TrendingUp, BarChart3, Zap, Brain, CloudRain } from 'lucide-react';

const Home = () => {
  const [healthStatus, setHealthStatus] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [health, models] = await Promise.all([
        weatherAPI.healthCheck(),
        weatherAPI.getModelInfo(),
      ]);
      setHealthStatus(health.data);
      setModelInfo(models.data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const features = [
    {
      icon: Target,
      title: 'Accurate Predictions',
      description: 'Get precise temperature predictions using state-of-the-art ML models',
      link: '/predict',
      color: 'text-blue-500',
      bgColor: 'bg-blue-50',
    },
    {
      icon: TrendingUp,
      title: 'Multi-hour Forecast',
      description: 'Generate forecasts up to 7 days ahead with detailed analytics',
      link: '/forecast',
      color: 'text-green-500',
      bgColor: 'bg-green-50',
    },
    {
      icon: BarChart3,
      title: 'Model Comparison',
      description: 'Compare predictions from multiple ML models side-by-side',
      link: '/compare',
      color: 'text-purple-500',
      bgColor: 'bg-purple-50',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-blue-500 rounded-full">
              <CloudRain className="h-16 w-16 text-white" />
            </div>
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Weather Forecasting ML
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Advanced machine learning powered weather prediction system using
            XGBoost, Random Forest, and Linear Regression models
          </p>
          
          {/* Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-center mb-2">
                <Brain className="h-8 w-8 text-blue-500 mr-2" />
                <span className="text-2xl font-bold text-gray-800">
                  {modelInfo?.models?.length || 0}
                </span>
              </div>
              <p className="text-gray-600">ML Models Loaded</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-center mb-2">
                <Zap className="h-8 w-8 text-green-500 mr-2" />
                <span className={`text-2xl font-bold ${
                  healthStatus?.models_loaded ? 'text-green-500' : 'text-red-500'
                }`}>
                  {healthStatus?.models_loaded ? 'Ready' : 'Loading'}
                </span>
              </div>
              <p className="text-gray-600">System Status</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-center mb-2">
                <Target className="h-8 w-8 text-purple-500 mr-2" />
                <span className="text-2xl font-bold text-gray-800">
                  {modelInfo?.num_features || 0}
                </span>
              </div>
              <p className="text-gray-600">Features Analyzed</p>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {features.map((feature, index) => (
            <Link
              key={index}
              to={feature.link}
              className="bg-white rounded-xl shadow-lg p-8 card-hover"
            >
              <div className={`inline-flex p-3 rounded-lg ${feature.bgColor} mb-4`}>
                <feature.icon className={`h-8 w-8 ${feature.color}`} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 mb-4">
                {feature.description}
              </p>
              <span className={`inline-flex items-center font-semibold ${feature.color}`}>
                Try it now →
              </span>
            </Link>
          ))}
        </div>

        {/* Model Performance Section */}
        {modelInfo?.performance && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
              Model Performance Metrics
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {Object.entries(modelInfo.performance).map(([model, metrics]) => (
                <div key={model} className="border rounded-lg p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">{model}</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">MAE:</span>
                      <span className="font-semibold">{metrics.MAE?.toFixed(3)}°C</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">RMSE:</span>
                      <span className="font-semibold">{metrics.RMSE?.toFixed(3)}°C</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">R² Score:</span>
                      <span className="font-semibold text-green-600">
                        {(metrics.R2 * 100)?.toFixed(2)}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
