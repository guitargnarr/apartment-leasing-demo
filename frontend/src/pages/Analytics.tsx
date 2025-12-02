import { useQuery } from '@tanstack/react-query';
import { TrendingUp, BarChart3, PieChart as PieChartIcon, Activity } from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { Card, CardHeader, CardContent } from '../components/Card';
import { analyticsApi } from '../utils/api';

const COLORS = ['#14b8a6', '#f97316', '#64748b', '#8b5cf6', '#ec4899'];

export function Analytics() {
  const { data: analytics, isLoading: analyticsLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: analyticsApi.getDashboard,
  });

  const { data: distribution, isLoading: distributionLoading } = useQuery({
    queryKey: ['distribution'],
    queryFn: analyticsApi.getDistribution,
  });

  const { data: trends, isLoading: trendsLoading } = useQuery({
    queryKey: ['trends'],
    queryFn: () => analyticsApi.getTrends(30),
  });

  const isLoading = analyticsLoading || distributionLoading || trendsLoading;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-500"></div>
      </div>
    );
  }

  const statusData =
    distribution?.status_distribution?.map((item) => ({
      name: item.status.charAt(0).toUpperCase() + item.status.slice(1),
      value: item.count,
    })) || [];

  const bedroomData =
    distribution?.bedroom_distribution?.map((item) => ({
      name: item.bedrooms === 0 ? 'Studio' : `${item.bedrooms} BR`,
      count: item.count,
    })) || [];

  const cityData =
    distribution?.city_distribution?.slice(0, 5).map((item) => ({
      name: item.city,
      count: item.count,
    })) || [];

  const priceTrends = trends?.trends || analytics?.price_trends || [];

  const featureData =
    analytics?.most_popular_features?.slice(0, 8).map((item) => ({
      name: item.feature,
      count: item.count,
    })) || [];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Analytics</h1>
        <p className="text-slate-400 mt-1">
          Detailed insights into your apartment listings
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Conversion Rate</p>
              <p className="text-2xl font-bold text-white mt-1">
                {((analytics?.lease_conversion_rate || 0) * 100).toFixed(1)}%
              </p>
            </div>
            <div className="bg-teal-500/10 p-3 rounded-lg">
              <TrendingUp className="h-6 w-6 text-teal-400" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Avg. Days to Lease</p>
              <p className="text-2xl font-bold text-white mt-1">
                {Math.round(analytics?.average_days_to_lease || 0)}
              </p>
            </div>
            <div className="bg-orange-500/10 p-3 rounded-lg">
              <Activity className="h-6 w-6 text-orange-400" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Average Price</p>
              <p className="text-2xl font-bold text-white mt-1">
                ${(analytics?.average_price || 0).toLocaleString()}
              </p>
            </div>
            <div className="bg-teal-500/10 p-3 rounded-lg">
              <BarChart3 className="h-6 w-6 text-teal-400" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Total Units</p>
              <p className="text-2xl font-bold text-white mt-1">
                {analytics?.total_units || 0}
              </p>
            </div>
            <div className="bg-orange-500/10 p-3 rounded-lg">
              <PieChartIcon className="h-6 w-6 text-orange-400" />
            </div>
          </div>
        </Card>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Price Trends */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">Price Trends (30 Days)</h2>
          </CardHeader>
          <CardContent>
            {priceTrends.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={priceTrends}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis
                    dataKey="date"
                    stroke="#94a3b8"
                    tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  />
                  <YAxis
                    stroke="#94a3b8"
                    tickFormatter={(value) => `$${value.toLocaleString()}`}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                    }}
                    formatter={(value: number) => [`$${value.toLocaleString()}`, 'Avg Price']}
                    labelFormatter={(label) => new Date(label).toLocaleDateString()}
                  />
                  <Line
                    type="monotone"
                    dataKey="average_price"
                    stroke="#14b8a6"
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 6, fill: '#14b8a6' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-slate-400">
                No trend data available
              </div>
            )}
          </CardContent>
        </Card>

        {/* Status Distribution */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">Unit Status Distribution</h2>
          </CardHeader>
          <CardContent>
            {statusData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={110}
                    paddingAngle={3}
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
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-slate-400">
                No status data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bedroom Distribution */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">Units by Bedroom Count</h2>
          </CardHeader>
          <CardContent>
            {bedroomData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={bedroomData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
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
              <div className="h-[300px] flex items-center justify-center text-slate-400">
                No bedroom data available
              </div>
            )}
          </CardContent>
        </Card>

        {/* City Distribution */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-white">Top Cities</h2>
          </CardHeader>
          <CardContent>
            {cityData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={cityData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis type="number" stroke="#94a3b8" />
                  <YAxis dataKey="name" type="category" stroke="#94a3b8" width={100} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                    }}
                  />
                  <Bar dataKey="count" fill="#f97316" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-slate-400">
                No city data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Popular Features */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-semibold text-white">Most Popular Amenities</h2>
        </CardHeader>
        <CardContent>
          {featureData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={featureData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" angle={-45} textAnchor="end" height={80} />
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
            <div className="h-[300px] flex items-center justify-center text-slate-400">
              No feature data available
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
