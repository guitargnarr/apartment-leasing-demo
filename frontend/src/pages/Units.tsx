import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Search, Filter, ChevronDown, ExternalLink, Trash2 } from 'lucide-react';
import { unitsApi } from '../utils/api';
import { StatusBadge } from '../components/StatusBadge';
import { LeadScoreBadge } from '../components/LeadScoreBadge';
import { Card } from '../components/Card';
import { useWebSocket } from '../hooks/useWebSocket';
import { ToastContainer } from '../components/Toast';
import type { Unit, UnitFilters, UnitStatus } from '../types';

export function Units() {
  const queryClient = useQueryClient();
  const [filters, setFilters] = useState<UnitFilters>({});
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [toasts, setToasts] = useState<Array<{ id: string; message: string; type: 'success' | 'error' | 'info' }>>([]);

  const addToast = useCallback((message: string, type: 'success' | 'error' | 'info') => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type }]);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  // WebSocket for real-time updates
  useWebSocket(
    useCallback(
      (unit: Unit) => {
        queryClient.invalidateQueries({ queryKey: ['units'] });
        addToast(`Unit "${unit.property_name}" updated`, 'info');
      },
      [queryClient, addToast]
    )
  );

  const { data, isLoading, error } = useQuery({
    queryKey: ['units', filters],
    queryFn: () => unitsApi.getUnits(filters),
  });

  const deleteMutation = useMutation({
    mutationFn: unitsApi.deleteUnit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
      addToast('Unit deleted successfully', 'success');
    },
    onError: () => {
      addToast('Failed to delete unit', 'error');
    },
  });

  const handleFilterChange = (key: keyof UnitFilters, value: string | number | undefined) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value || undefined,
    }));
  };

  const filteredUnits = data?.units?.filter((unit) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return (
      unit.property_name.toLowerCase().includes(query) ||
      unit.location.city.toLowerCase().includes(query) ||
      unit.location.address.toLowerCase().includes(query)
    );
  });

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-400">
          Error loading units. Make sure the backend is running at localhost:8000
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <ToastContainer toasts={toasts} onClose={removeToast} />

      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Units</h1>
          <p className="text-slate-400 mt-1">
            {data?.total || 0} total units
          </p>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search by property name, city, or address..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          />
        </div>

        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2 px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-300 hover:bg-slate-700 transition-colors"
        >
          <Filter className="h-5 w-5" />
          <span>Filters</span>
          <ChevronDown className={`h-4 w-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {/* Filter Panel */}
      {showFilters && (
        <Card className="p-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Status</label>
              <select
                value={filters.status || ''}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-teal-500"
              >
                <option value="">All Statuses</option>
                <option value="available">Available</option>
                <option value="pending">Pending</option>
                <option value="leased">Leased</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Bedrooms</label>
              <select
                value={filters.bedrooms || ''}
                onChange={(e) => handleFilterChange('bedrooms', e.target.value ? parseInt(e.target.value) : undefined)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-teal-500"
              >
                <option value="">Any</option>
                <option value="0">Studio</option>
                <option value="1">1 BR</option>
                <option value="2">2 BR</option>
                <option value="3">3 BR</option>
                <option value="4">4+ BR</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Min Price</label>
              <input
                type="number"
                placeholder="$0"
                value={filters.price_min || ''}
                onChange={(e) => handleFilterChange('price_min', e.target.value ? parseInt(e.target.value) : undefined)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Max Price</label>
              <input
                type="number"
                placeholder="$10,000"
                value={filters.price_max || ''}
                onChange={(e) => handleFilterChange('price_max', e.target.value ? parseInt(e.target.value) : undefined)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
          </div>

          <div className="mt-4 flex justify-end">
            <button
              onClick={() => setFilters({})}
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </Card>
      )}

      {/* Units Table */}
      <Card>
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-500"></div>
          </div>
        ) : filteredUnits && filteredUnits.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left px-6 py-4 text-sm font-medium text-slate-400">Property</th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-slate-400">Location</th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-slate-400">Details</th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-slate-400">Price</th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-slate-400">Status</th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-slate-400">Lead Score</th>
                  <th className="text-right px-6 py-4 text-sm font-medium text-slate-400">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUnits.map((unit) => (
                  <tr
                    key={unit.id}
                    className="border-b border-slate-700/50 hover:bg-slate-800/50 transition-colors"
                  >
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white font-medium">{unit.property_name}</p>
                        <p className="text-slate-400 text-sm">Unit {unit.unit_number}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-slate-300">{unit.location.city}, {unit.location.state}</p>
                        <p className="text-slate-500 text-sm">{unit.location.address}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-slate-300">
                        {unit.bedrooms} BR / {unit.bathrooms} BA
                      </p>
                      <p className="text-slate-500 text-sm">{unit.square_feet.toLocaleString()} sq ft</p>
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-white font-medium">${unit.price.toLocaleString()}</p>
                      <p className="text-slate-500 text-sm">/month</p>
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={unit.status as UnitStatus} />
                    </td>
                    <td className="px-6 py-4">
                      <LeadScoreBadge score={unit.lead_score} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          to={`/units/${unit.id}`}
                          className="p-2 text-slate-400 hover:text-teal-400 transition-colors"
                          title="View Details"
                        >
                          <ExternalLink className="h-4 w-4" />
                        </Link>
                        <button
                          onClick={() => {
                            if (confirm('Are you sure you want to delete this unit?')) {
                              deleteMutation.mutate(unit.id);
                            }
                          }}
                          className="p-2 text-slate-400 hover:text-red-400 transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-64 text-slate-400">
            <p>No units found</p>
            <p className="text-sm mt-1">Try adjusting your filters or search query</p>
          </div>
        )}
      </Card>
    </div>
  );
}
