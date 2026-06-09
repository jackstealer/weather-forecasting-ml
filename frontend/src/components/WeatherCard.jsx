import React from 'react';
import { Thermometer, Droplets, Wind, Gauge, Eye, Compass } from 'lucide-react';

function WeatherCard({ weather }) {
  const metrics = [
    { label: 'Temperature', value: `${weather.temperature.toFixed(1)}°C`, icon: Thermometer },
    { label: 'Feels Like', value: `${weather.feels_like.toFixed(1)}°C`, icon: Thermometer },
    { label: 'Humidity', value: `${weather.humidity}%`, icon: Droplets },
    { label: 'Pressure', value: `${weather.pressure} hPa`, icon: Gauge },
    { label: 'Wind Speed', value: `${weather.wind_speed} m/s`, icon: Wind },
    { label: 'Wind Direction', value: `${weather.wind_direction}°`, icon: Compass },
    { label: 'Visibility', value: `${(weather.visibility / 1000).toFixed(1)} km`, icon: Eye },
    { label: 'Conditions', value: weather.weather_description, icon: null },
  ];

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-gray-800">
          🌤️ Current Weather
        </h3>
        <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
          Live Data
        </span>
      </div>
      
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <div
              key={index}
              className="bg-white/60 p-4 rounded-xl border border-gray-100 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center space-x-2 mb-2">
                {Icon && <Icon className="w-4 h-4 text-gray-500" />}
                <span className="text-sm text-gray-600 font-medium">{metric.label}</span>
              </div>
              <p className="text-lg font-bold text-gray-800 capitalize">{metric.value}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default WeatherCard;
