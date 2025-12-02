import { useQuery } from '@tanstack/react-query';
import { Building2, CheckCircle, Clock, DollarSign, TrendingUp, Activity } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { StatCard } from '../components/StatCard';
import { Card, CardHeader, CardContent } from '../components/Card';
import { analyticsApi, leadScoringApi } from '../utils/api';
import { LeadScoreBadge } from '../components/LeadScoreBadge';
import type { Unit } from '../types';

const COLORS = ['#14b8a6', '#f97316', '#64748b'];

export function Dashboard() {
  const { data: analytics, isLoading: analyticsLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: analyticsApi.getDashboard,
  });

  const { data: distribution, isLoading: distributionLoading } = useQuery({
    queryKey: ['distribution'],
    queryFn: analyticsApi.getDistribution,
  });

  const { data: prioritizedUnits, isLoading: prioritizedLoading } = useQuery({
    queryKey: ['prioritizedUnits'],
    queryFn: () => leadScoringApi.getPrioritizedUnits(5),
  });

  if (analyticsLoading || distributionLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-500"></div>
      </div>
    );
  }

  const statusData = distribution?.status_distribution?.map((item) => ({
    name: item.status.charAt(0).toUpperCase() + item.status.slice(1),
    value: item.count,
  })) || [];

  const bedroomData = distribution?.bedroom_distribution?.map((item) => ({
    name: `${item.bedrooms} BR`,
    count: item.count,
  })) || [];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400 mt-1">Overview of your apartment listings</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Units"
          value={analytics?.total_units || 0}
          icon={Building2}
        />
        <StatCard
          title="Available"
          value={analytics?.available_units || 0}
          icon={CheckCircle}
          change={`${Math.round((analytics?.available_units || 0) / (analytics?.total_units || 1) * 100)}% of total`}
          changeType="positive"
        />
        <StatCard
          title="Avg. Days to Lease"
          value={Math.round(analytics?.average_days_to_lease || 0)}
          icon={Clock}
        />
        <StatCard
          title="Avg. Price"
          value={`$${(analytics?.average_price || 0).toLocaleString()}`}
          icon={DollarSign}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Status Distribution */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">Unit Status Distribution</h2>
          </CardHeader>
          <CardContent>
            {statusData.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(0)}%`}
                  >
                    {statusData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[250px] flex items-center justify-center text-slate-400">
                No data available
              </div>
            )}
          </CardContent>
        </Card>

        {/* Bedroom Distribution */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">Units by Bedroom</h2>
          </CardHeader>
          <CardContent>
            {bedroomData.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={bedroomData}>
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                    }}
                  />
                  <Bar dataKey="count" fill="#14b8a6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[250px] flex items-center justify-center text-slate-400">
                No data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Conversion Metrics */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-teal-500" />
              <h2 className="text-lg font-semibold text-white">Performance Metrics</h2>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Lease Conversion Rate</span>
                <span className="text-xl font-semibold text-white">
                  {((analytics?.lease_conversion_rate || 0) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div
                  className="bg-teal-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${(analytics?.lease_conversion_rate || 0) * 100}%` }}
                />
              </div>

              <div className="mt-6 space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">Available Units</span>
                  <span className="text-teal-400 font-medium">{analytics?.available_units}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">Pending Leases</span>
                  <span className="text-orange-400 font-medium">{analytics?.pending_units}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">Leased Units</span>
                  <span className="text-slate-400 font-medium">{analytics?.leased_units}</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Hot Leads */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-orange-500" />
              <h2 className="text-lg font-semibold text-white">Priority Units</h2>
            </div>
          </CardHeader>
          <CardContent>
            {prioritizedLoading ? (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-teal-500"></div>
              </div>
            ) : prioritizedUnits && prioritizedUnits.length > 0 ? (
              <div className="space-y-3">
                {prioritizedUnits.map((unit: Unit) => (
                  <div
                    key={unit.id}
                    className="flex items-center justify-between p-3 bg-slate-900 rounded-lg"
                  >
                    <div>
                      <p className="text-white font-medium">{unit.property_name}</p>
                      <p className="text-slate-400 text-sm">
                        {unit.bedrooms}BR / {unit.bathrooms}BA - ${unit.price.toLocaleString()}/mo
                      </p>
                    </div>
                    <LeadScoreBadge score={unit.lead_score} />
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex items-center justify-center h-40 text-slate-400">
                No priority units available
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
