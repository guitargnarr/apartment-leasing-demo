import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, MapPin, Bed, Bath, Square, DollarSign, Calendar, Tag } from 'lucide-react';
import { unitsApi, leadScoringApi } from '../utils/api';
import { Card, CardHeader, CardContent } from '../components/Card';
import { StatusBadge } from '../components/StatusBadge';
import { LeadScoreBadge } from '../components/LeadScoreBadge';
import type { UnitStatus } from '../types';
import { useState } from 'react';

export function UnitDetail() {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const [selectedStatus, setSelectedStatus] = useState<UnitStatus | ''>('');

  const { data: unit, isLoading, error } = useQuery({
    queryKey: ['unit', id],
    queryFn: () => unitsApi.getUnit(id!),
    enabled: !!id,
  });

  const { data: leadScore } = useQuery({
    queryKey: ['leadScore', id],
    queryFn: () => leadScoringApi.getLeadScore(id!),
    enabled: !!id,
  });

  const updateMutation = useMutation({
    mutationFn: (updates: { status: UnitStatus }) => unitsApi.updateUnit(id!, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['unit', id] });
      queryClient.invalidateQueries({ queryKey: ['units'] });
      setSelectedStatus('');
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-500"></div>
      </div>
    );
  }

  if (error || !unit) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <p className="text-red-400">Unit not found</p>
        <Link to="/units" className="text-teal-400 hover:underline mt-2">
          Back to Units
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <Link
        to="/units"
        className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        <span>Back to Units</span>
      </Link>

      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">{unit.property_name}</h1>
          <div className="flex items-center gap-2 mt-2 text-slate-400">
            <MapPin className="h-4 w-4" />
            <span>
              {unit.location.address}, {unit.location.city}, {unit.location.state} {unit.location.zip}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <StatusBadge status={unit.status} />
          <LeadScoreBadge score={unit.lead_score} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Quick Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <Card className="p-4">
              <div className="flex items-center gap-3">
                <div className="bg-teal-500/10 p-2 rounded-lg">
                  <Bed className="h-5 w-5 text-teal-400" />
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Bedrooms</p>
                  <p className="text-white font-semibold">{unit.bedrooms}</p>
                </div>
              </div>
            </Card>

            <Card className="p-4">
              <div className="flex items-center gap-3">
                <div className="bg-teal-500/10 p-2 rounded-lg">
                  <Bath className="h-5 w-5 text-teal-400" />
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Bathrooms</p>
                  <p className="text-white font-semibold">{unit.bathrooms}</p>
                </div>
              </div>
            </Card>

            <Card className="p-4">
              <div className="flex items-center gap-3">
                <div className="bg-teal-500/10 p-2 rounded-lg">
                  <Square className="h-5 w-5 text-teal-400" />
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Sq Ft</p>
                  <p className="text-white font-semibold">{unit.square_feet.toLocaleString()}</p>
                </div>
              </div>
            </Card>

            <Card className="p-4">
              <div className="flex items-center gap-3">
                <div className="bg-orange-500/10 p-2 rounded-lg">
                  <DollarSign className="h-5 w-5 text-orange-400" />
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Price</p>
                  <p className="text-white font-semibold">${unit.price.toLocaleString()}/mo</p>
                </div>
              </div>
            </Card>
          </div>

          {/* Description */}
          <Card>
            <CardHeader>
              <h2 className="text-lg font-semibold text-white">Description</h2>
            </CardHeader>
            <CardContent>
              <p className="text-slate-300 leading-relaxed">{unit.description}</p>
            </CardContent>
          </Card>

          {/* Amenities */}
          <Card>
            <CardHeader>
              <h2 className="text-lg font-semibold text-white">Amenities</h2>
            </CardHeader>
            <CardContent>
              {unit.amenities.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {unit.amenities.map((amenity, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-full text-sm text-slate-300"
                    >
                      <Tag className="h-3.5 w-3.5 text-teal-400" />
                      {amenity}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-slate-500">No amenities listed</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Actions */}
          <Card>
            <CardHeader>
              <h2 className="text-lg font-semibold text-white">Update Status</h2>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <select
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value as UnitStatus)}
                  className="w-full px-3 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-teal-500"
                >
                  <option value="">Select new status</option>
                  <option value="available">Available</option>
                  <option value="pending">Pending</option>
                  <option value="leased">Leased</option>
                </select>
                <button
                  onClick={() => {
                    if (selectedStatus) {
                      updateMutation.mutate({ status: selectedStatus });
                    }
                  }}
                  disabled={!selectedStatus || updateMutation.isPending}
                  className="w-full py-2.5 bg-teal-500 hover:bg-teal-400 disabled:bg-slate-700 disabled:text-slate-500 text-white font-medium rounded-lg transition-colors"
                >
                  {updateMutation.isPending ? 'Updating...' : 'Update Status'}
                </button>
              </div>
            </CardContent>
          </Card>

          {/* Lead Score Breakdown */}
          {leadScore && (
            <Card>
              <CardHeader>
                <h2 className="text-lg font-semibold text-white">Lead Score Breakdown</h2>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center mb-4">
                    <span className="text-4xl font-bold text-white">
                      {Math.round(leadScore.lead_score)}
                    </span>
                    <span className="text-slate-400 text-sm ml-1">/100</span>
                  </div>

                  {leadScore.score_breakdown && (
                    <div className="space-y-3">
                      {Object.entries(leadScore.score_breakdown)
                        .filter(([key]) => key !== 'total_score')
                        .map(([key, value]) => (
                          <div key={key} className="flex items-center justify-between">
                            <span className="text-slate-400 text-sm capitalize">
                              {key.replace(/_/g, ' ')}
                            </span>
                            <span className="text-white font-medium">
                              {typeof value === 'number' ? Math.round(value) : value}
                            </span>
                          </div>
                        ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Dates */}
          <Card>
            <CardHeader>
              <h2 className="text-lg font-semibold text-white">Timeline</h2>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Calendar className="h-4 w-4 text-slate-400" />
                  <div>
                    <p className="text-slate-400 text-sm">Listed</p>
                    <p className="text-white">
                      {new Date(unit.date_listed).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                {unit.date_leased && (
                  <div className="flex items-center gap-3">
                    <Calendar className="h-4 w-4 text-teal-400" />
                    <div>
                      <p className="text-slate-400 text-sm">Leased</p>
                      <p className="text-white">
                        {new Date(unit.date_leased).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
