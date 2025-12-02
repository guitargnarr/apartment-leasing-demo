export interface Location {
  address: string;
  city: string;
  state: string;
  zip: string;
  lat: number;
  lng: number;
}

export type UnitStatus = 'available' | 'pending' | 'leased';

export interface Unit {
  id: string;
  property_name: string;
  unit_number: string;
  bedrooms: number;
  bathrooms: number;
  square_feet: number;
  price: number;
  status: UnitStatus;
  amenities: string[];
  location: Location;
  images: string[];
  description: string;
  lead_score: number;
  date_listed: string;
  date_leased: string | null;
  created_at: string;
  updated_at: string;
}

export interface UnitListResponse {
  units: Unit[];
  total: number;
  page: number;
  page_size: number;
}

export interface UnitFilters {
  status?: string;
  bedrooms?: number;
  price_min?: number;
  price_max?: number;
  city?: string;
}

export interface AnalyticsData {
  total_units: number;
  available_units: number;
  leased_units: number;
  pending_units: number;
  average_days_to_lease: number;
  lease_conversion_rate: number;
  average_price: number;
  most_popular_features: Array<{ feature: string; count: number }>;
  price_trends: Array<{ date: string; average_price: number }>;
}

export interface LeadScoreBreakdown {
  unit_id: string;
  lead_score: number;
  score_breakdown: {
    total_score: number;
    price_competitiveness: number;
    days_on_market: number;
    amenity_score: number;
    location_score: number;
  };
}

export interface DistributionData {
  bedroom_distribution: Array<{ bedrooms: number; count: number }>;
  status_distribution: Array<{ status: string; count: number }>;
  city_distribution: Array<{ city: string; count: number }>;
}

export interface WebSocketMessage {
  type: 'unit_update' | 'unit_deleted' | 'connected';
  data: Unit | { unit_id: string } | Record<string, unknown>;
}
