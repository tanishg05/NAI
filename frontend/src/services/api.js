import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const generateDietPlan = async (payload) => {
  const response = await api.post('/diet-plan/generate', payload);
  return response.data;
};

export const generateRecommendations = async (payload) => {
  const response = await api.post('/recommendations/generate', payload);
  return response.data;
};

export default api;
