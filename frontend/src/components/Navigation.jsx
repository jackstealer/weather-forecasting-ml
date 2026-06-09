import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Cloud, Target, TrendingUp, BarChart3 } from 'lucide-react';

const Navigation = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: Cloud },
    { path: '/predict', label: 'Predict', icon: Target },
    { path: '/forecast', label: 'Forecast', icon: TrendingUp },
    { path: '/compare', label: 'Compare', icon: BarChart3 },
  ];

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Cloud className="h-8 w-8 text-blue-500 mr-2" />
            <span className="text-2xl font-bold text-gray-800">
              Weather Forecasting ML
            </span>
          </div>
          
          <div className="flex space-x-4 items-center">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === path
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-700 hover:bg-blue-100'
                }`}
              >
                <Icon className="h-4 w-4 mr-2" />
                {label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
