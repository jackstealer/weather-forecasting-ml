import React from 'react';

const colorClasses = {
  red: 'from-red-400 to-red-600',
  blue: 'from-blue-400 to-blue-600',
  green: 'from-green-400 to-green-600',
  purple: 'from-purple-400 to-purple-600',
  orange: 'from-orange-400 to-orange-600',
  indigo: 'from-indigo-400 to-indigo-600',
};

function MetricCard({ title, value, icon: Icon, color = 'blue', unit = '°C' }) {
  return (
    <div className="metric-card">
      <div className="flex items-start justify-between mb-3">
        <div className={`p-2 rounded-lg bg-gradient-to-br ${colorClasses[color]}`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
      </div>
      <div className="space-y-1">
        <p className="text-sm text-gray-600 font-medium">{title}</p>
        <p className="text-3xl font-bold text-gray-800">
          {typeof value === 'number' ? value.toFixed(1) : value}
          <span className="text-lg text-gray-500 ml-1">{unit}</span>
        </p>
      </div>
    </div>
  );
}

export default MetricCard;
