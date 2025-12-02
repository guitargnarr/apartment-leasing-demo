import axios from 'axios';
import type { Unit, UnitListResponse, UnitFilters, AnalyticsData, LeadScoreBreakdown, DistributionData } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const unitsApi = {
  getUnits: async (filters?: UnitFilters, skip = 0, limit = 100): Promise<UnitListResponse> => {
    const params = new URLSearchParams();
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());

    if (filters?.status) params.append('status', filters.status);
    if (filters?.bedrooms) params.append('bedrooms', filters.bedrooms.toString());
    if (filters?.price_min) params.append('price_min', filters.price_min.toString());
    if (filters?.price_max) params.append('price_max', filters.price_max.toString());
    if (filters?.city) params.append('city', filters.city);

    const response = await api.get<UnitListResponse>(`/api/units?${params}`);
    return response.data;
  },

  getUnit: async (unitId: string): Promise<Unit> => {
    const response = await api.get<Unit>(`/api/units/${unitId}`);
    return response.data;
  },

  createUnit: async (unit: Omit<Unit, 'id' | 'lead_score' | 'date_listed' | 'date_leased' | 'created_at' | 'updated_at'>): Promise<Unit> => {
    const response = await api.post<Unit>('/api/units', unit);
    return response.data;
  },

  updateUnit: async (unitId: string, updates: Partial<Unit>): Promise<Unit> => {
    const response = await api.patch<Unit>(`/api/units/${unitId}`, updates);
    return response.data;
  },

  deleteUnit: async (unitId: string): Promise<void> => {
    await api.delete(`/api/units/${unitId}`);
  },
};

export const analyticsApi = {
  getDashboard: async (): Promise<AnalyticsData> => {
    const response = await api.get<AnalyticsData>('/api/analytics');
    return response.data;
  },

  getTrends: async (days = 30): Promise<{ trends: Array<{ date: string; average_price: number }> }> => {
    const response = await api.get(`/api/analytics/trends?days=${days}`);
    return response.data;
  },

  getDistribution: async (): Promise<DistributionData> => {
    const response = await api.get<DistributionData>('/api/analytics/distribution');
    return response.data;
  },
};

export const leadScoringApi = {
  getLeadScore: async (unitId: string): Promise<LeadScoreBreakdown> => {
    const response = await api.get<LeadScoreBreakdown>(`/api/leads/score/${unitId}`);
    return response.data;
  },

  getPrioritizedUnits: async (limit = 50): Promise<Unit[]> => {
    const response = await api.get<Unit[]>(`/api/leads/prioritized?limit=${limit}`);
    return response.data;
  },

  recalculateScores: async (): Promise<{ message: string; updated_count: number }> => {
    const response = await api.post('/api/leads/recalculate');
    return response.data;
  },
};

export const healthApi = {
  check: async (): Promise<{ status: string; database: string; websocket_connections: number }> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
