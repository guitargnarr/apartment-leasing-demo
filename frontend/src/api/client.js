import axios from 'axios';

// API base URL - defaults to localhost, override with env variable for production
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Units API
export const unitsAPI = {
  getAll: (params = {}) => api.get('/api/units', { params }),
  getById: (id) => api.get(`/api/units/${id}`),
  create: (data) => api.post('/api/units', data),
  update: (id, data) => api.patch(`/api/units/${id}`, data),
  delete: (id) => api.delete(`/api/units/${id}`),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/api/analytics'),
  getTrends: (days = 30) => api.get(`/api/analytics/trends?days=${days}`),
  getDistribution: () => api.get('/api/analytics/distribution'),
  getPerformance: () => api.get('/api/analytics/performance'),
};

// Lead Scoring API
export const leadsAPI = {
  getScore: (unitId) => api.get(`/api/leads/score/${unitId}`),
  getPrioritized: (limit = 50) => api.get(`/api/leads/prioritized?limit=${limit}`),
  recalculate: () => api.post('/api/leads/recalculate'),
};

// Health Check
export const healthAPI = {
  check: () => api.get('/health'),
  root: () => api.get('/'),
};

export default api;
