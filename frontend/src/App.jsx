import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Cloud, Activity, BarChart3, Github, Zap } from 'lucide-react';
import PredictPage from './pages/PredictPage';
import ForecastPage from './pages/ForecastPage';
import ComparePage from './pages/ComparePage';
import { weatherAPI } from './services/api';

function Navigation() {
  const location = useLocation();
  const [apiStatus, setApiStatus] = useState({ loading: true, healthy: false });

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await weatherAPI.healthCheck();
        setApiStatus({ loading: false, healthy: data.status === 'healthy' });
      } catch (error) {
        setApiStatus({ loading: false, healthy: false });
      }
    };
    checkHealth();
  }, []);

  const navItems = [
    { path: '/', label: 'Predict', icon: Cloud },
    { path: '/forecast', label: 'Forecast', icon: Activity },
    { path: '/compare', label: 'Compare', icon: BarChart3 },
  ];

  return (
    <nav className="glass-card sticky top-6 z-50 mx-6 mb-6 shadow-2xl">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl blur-lg opacity-50"></div>
              <div className="relative bg-gradient-to-br from-blue-500 to-indigo-600 p-3 rounded-xl">
                <Cloud className="w-6 h-6 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Weather AI
              </h1>
              <p className="text-xs text-gray-500">ML-Powered Forecasting</p>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`tab-button ${isActive ? 'tab-active' : 'tab-inactive'}`}
                >
                  <div className="flex items-center space-x-2">
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </div>
                </Link>
              );
            })}
          </div>

          {/* Status Indicator */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              {apiStatus.loading ? (
                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
              ) : apiStatus.healthy ? (
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              ) : (
                <div className="w-2 h-2 bg-red-400 rounded-full"></div>
              )}
              <span className="text-xs text-gray-600">
                {apiStatus.loading ? 'Checking...' : apiStatus.healthy ? 'Online' : 'Offline'}
              </span>
            </div>
            <div className="flex items-center space-x-1 text-xs text-gray-500">
              <Zap className="w-3 h-3" />
              <span>XGBoost</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen pb-12">
        <div className="pt-6">
          <Navigation />
          
          {/* Help Banner */}
          <div className="max-w-7xl mx-auto px-6 mb-4">
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-500 p-2 rounded-lg">
                  <Cloud className="w-5 h-5 text-white" />
                </div>
                <div>
                  <div className="font-semibold text-gray-800">Welcome to Weather AI!</div>
                  <div className="text-sm text-gray-600">Get instant temperature predictions powered by artificial intelligence</div>
                </div>
              </div>
            </div>
          </div>
          
          <main className="max-w-7xl mx-auto px-6">
            <Routes>
              <Route path="/" element={<PredictPage />} />
              <Route path="/forecast" element={<ForecastPage />} />
              <Route path="/compare" element={<ComparePage />} />
            </Routes>
          </main>
        </div>

        {/* Footer */}
        <footer className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-t border-gray-200 py-3">
          <div className="max-w-7xl mx-auto px-6 flex items-center justify-between text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <span>Powered by React + Flask + XGBoost</span>
            </div>
            <div className="flex items-center space-x-4">
              <span>1.6M+ training samples</span>
              <span>•</span>
              <span>86% accuracy</span>
              <span>•</span>
              <span>250+ cities</span>
            </div>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-1 hover:text-blue-600 transition-colors"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </a>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
