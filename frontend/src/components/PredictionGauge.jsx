import React from 'react';

function PredictionGauge({ value, actual }) {
  const minTemp = -20;
  const maxTemp = 50;
  const range = maxTemp - minTemp;
  const percentage = ((value - minTemp) / range) * 100;
  
  const getColor = (temp) => {
    if (temp < 0) return '#3b82f6'; // blue
    if (temp < 10) return '#60a5fa'; // light blue
    if (temp < 20) return '#34d399'; // green
    if (temp < 30) return '#fbbf24'; // yellow
    if (temp < 40) return '#fb923c'; // orange
    return '#ef4444'; // red
  };

  const color = getColor(value);
  const actualPercentage = actual ? ((actual - minTemp) / range) * 100 : null;

  return (
    <div className="space-y-6">
      {/* Gauge Bar */}
      <div className="relative h-32">
        {/* Background gradient */}
        <div className="absolute inset-0 rounded-full overflow-hidden">
          <div
            className="h-full w-full"
            style={{
              background: 'linear-gradient(to right, #3b82f6, #60a5fa, #34d399, #fbbf24, #fb923c, #ef4444)',
            }}
          />
        </div>
        
        {/* Prediction marker */}
        <div
          className="absolute top-0 bottom-0 w-2 bg-white border-4 border-gray-800 rounded-full shadow-xl transition-all duration-500"
          style={{ left: `calc(${percentage}% - 4px)` }}
        >
          <div className="absolute -top-12 left-1/2 -translate-x-1/2 bg-gray-800 text-white px-3 py-1 rounded-lg text-sm font-bold whitespace-nowrap">
            {value.toFixed(1)}°C
          </div>
        </div>
        
        {/* Actual temperature marker (if available) */}
        {actual && (
          <div
            className="absolute top-0 bottom-0 w-2 bg-white border-4 border-green-500 rounded-full shadow-xl"
            style={{ left: `calc(${actualPercentage}% - 4px)` }}
          >
            <div className="absolute -bottom-12 left-1/2 -translate-x-1/2 bg-green-500 text-white px-3 py-1 rounded-lg text-sm font-bold whitespace-nowrap">
              Actual: {actual.toFixed(1)}°C
            </div>
          </div>
        )}
      </div>

      {/* Scale labels */}
      <div className="flex justify-between text-sm text-gray-600 font-medium px-1 mt-8">
        <span>{minTemp}°C</span>
        <span>0°C</span>
        <span>25°C</span>
        <span>{maxTemp}°C</span>
      </div>

      {/* Temperature zones */}
      <div className="grid grid-cols-6 gap-2 text-xs text-center">
        <div className="space-y-1">
          <div className="h-3 bg-blue-500 rounded"></div>
          <span className="text-gray-600">Freezing</span>
        </div>
        <div className="space-y-1">
          <div className="h-3 bg-blue-300 rounded"></div>
          <span className="text-gray-600">Cold</span>
        </div>
        <div className="space-y-1">
          <div className="h-3 bg-green-400 rounded"></div>
          <span className="text-gray-600">Cool</span>
        </div>
        <div className="space-y-1">
          <div className="h-3 bg-yellow-400 rounded"></div>
          <span className="text-gray-600">Warm</span>
        </div>
        <div className="space-y-1">
          <div className="h-3 bg-orange-400 rounded"></div>
          <span className="text-gray-600">Hot</span>
        </div>
        <div className="space-y-1">
          <div className="h-3 bg-red-500 rounded"></div>
          <span className="text-gray-600">Very Hot</span>
        </div>
      </div>

      {/* Difference indicator */}
      {actual && (
        <div className="glass-card p-4 text-center">
          <div className="text-sm text-gray-600 mb-1">Prediction vs Actual</div>
          <div className={`text-2xl font-bold ${Math.abs(value - actual) < 2 ? 'text-green-600' : Math.abs(value - actual) < 5 ? 'text-yellow-600' : 'text-red-600'}`}>
            {Math.abs(value - actual).toFixed(1)}°C difference
          </div>
        </div>
      )}
    </div>
  );
}

export default PredictionGauge;
