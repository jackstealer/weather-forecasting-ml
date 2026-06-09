import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    throw error.response?.data || { error: error.message };
  }
);

export const weatherAPI = {
  // Health check
  healthCheck: async () => {
    return await apiClient.get('/health');
  },

  // Get model information
  getModelInfo: async () => {
    return await apiClient.get('/models/info');
  },

  // Make prediction
  predict: async (data) => {
    return await apiClient.post('/predict', data);
  },

  // Generate forecast
  forecast: async (data) => {
    return await apiClient.post('/forecast', data);
  },

  // Get weather by city
  getWeatherByCity: async (city) => {
    return await apiClient.get(`/weather/city/${city}`);
  },

  // Get weather by coordinates
  getWeatherByCoordinates: async (latitude, longitude) => {
    return await apiClient.post('/weather/coordinates', { latitude, longitude });
  },

  // Get default cities
  getCities: async () => {
    return await apiClient.get('/cities');
  },
};

export default apiClient;
