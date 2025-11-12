import { useState, useEffect } from 'react';
import { unitsAPI, analyticsAPI, healthAPI } from './api/client';

function App() {
  const [units, setUnits] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('units');
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    checkAPI();
    loadData();
  }, [view]);

  const checkAPI = async () => {
    try {
      await healthAPI.root();
      setApiStatus('connected');
    } catch (error) {
      setApiStatus('disconnected');
      console.error('API connection failed:', error);
    }
  };

  const loadData = async () => {
    setLoading(true);
    try {
      if (view === 'units') {
        const response = await unitsAPI.getAll({ status: 'available' });
        setUnits(response.data.units || []);
      } else {
        const response = await analyticsAPI.getDashboard();
        setAnalytics(response.data);
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => `$${price.toLocaleString()}`;

  const getStatusBadge = (status) => {
    const classes = {
      available: 'badge-available',
      pending: 'badge-pending',
      leased: 'badge-leased'
    };
    return <span className={`badge ${classes[status]}`}>{status.toUpperCase()}</span>;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-primary-600">🏢 LeaseFlow</h1>
              <p className="text-sm text-gray-600">Intelligent Apartment Leasing Platform</p>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${apiStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-gray-600">{apiStatus === 'connected' ? 'API Connected' : 'API Disconnected'}</span>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setView('units')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                view === 'units'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Available Units
            </button>
            <button
              onClick={() => setView('analytics')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                view === 'analytics'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Analytics Dashboard
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading...</p>
            </div>
          </div>
        ) : view === 'units' ? (
          <div>
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Available Units ({units.length})</h2>
              <p className="text-gray-600">Browse available apartments in Louisville, KY</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {units.map((unit) => (
                <div key={unit.id} className="card hover:shadow-lg transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{unit.property_name}</h3>
                      <p className="text-sm text-gray-600">{unit.location.city}, {unit.location.state}</p>
                    </div>
                    {getStatusBadge(unit.status)}
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Price</span>
                      <span className="font-semibold text-primary-600">{formatPrice(unit.price)}/mo</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Bedrooms</span>
                      <span className="font-medium">{unit.bedrooms} bed</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Bathrooms</span>
                      <span className="font-medium">{unit.bathrooms} bath</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Square Feet</span>
                      <span className="font-medium">{unit.square_feet.toLocaleString()} sq ft</span>
                    </div>
                  </div>

                  {unit.lead_score && (
                    <div className="mb-4">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Lead Score</span>
                        <span className="font-medium">{unit.lead_score.toFixed(1)}/100</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            unit.lead_score >= 80 ? 'bg-green-500' :
                            unit.lead_score >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${unit.lead_score}%` }}
                        ></div>
                      </div>
                    </div>
                  )}

                  {unit.amenities && unit.amenities.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-500 mb-2">Amenities:</p>
                      <div className="flex flex-wrap gap-1">
                        {unit.amenities.slice(0, 3).map((amenity, idx) => (
                          <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                            {amenity}
                          </span>
                        ))}
                        {unit.amenities.length > 3 && (
                          <span className="text-xs text-gray-500">+{unit.amenities.length - 3} more</span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
            {units.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-600">No units available at this time.</p>
              </div>
            )}
          </div>
        ) : (
          <div>
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
              <p className="text-gray-600">Real-time metrics and performance indicators</p>
            </div>
            {analytics && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="card">
                    <p className="text-sm text-gray-600">Total Units</p>
                    <p className="text-3xl font-bold text-gray-900">{analytics.total_units}</p>
                  </div>
                  <div className="card">
                    <p className="text-sm text-gray-600">Available</p>
                    <p className="text-3xl font-bold text-green-600">{analytics.available_units}</p>
                  </div>
                  <div className="card">
                    <p className="text-sm text-gray-600">Leased</p>
                    <p className="text-3xl font-bold text-blue-600">{analytics.leased_units}</p>
                  </div>
                  <div className="card">
                    <p className="text-sm text-gray-600">Pending</p>
                    <p className="text-3xl font-bold text-yellow-600">{analytics.pending_units}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="card">
                    <p className="text-sm text-gray-600">Avg Days to Lease</p>
                    <p className="text-2xl font-bold text-gray-900">{analytics.average_days_to_lease.toFixed(1)} days</p>
                  </div>
                  <div className="card">
                    <p className="text-sm text-gray-600">Conversion Rate</p>
                    <p className="text-2xl font-bold text-gray-900">{analytics.lease_conversion_rate.toFixed(1)}%</p>
                  </div>
                  <div className="card">
                    <p className="text-sm text-gray-600">Avg Price</p>
                    <p className="text-2xl font-bold text-gray-900">{formatPrice(Math.round(analytics.average_price))}</p>
                  </div>
                </div>

                {analytics.most_popular_features && analytics.most_popular_features.length > 0 && (
                  <div className="card">
                    <h3 className="text-lg font-semibold mb-4">Most Popular Features</h3>
                    <div className="space-y-3">
                      {analytics.most_popular_features.slice(0, 5).map((feature, idx) => (
                        <div key={idx} className="flex items-center justify-between">
                          <span className="text-gray-700">{feature.feature}</span>
                          <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-600">
                              Leased: {feature.leased_count} | Available: {feature.available_count}
                            </span>
                            <span className="font-semibold text-primary-600">
                              {(feature.popularity_ratio * 100).toFixed(0)}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            LeaseFlow - Intelligent Apartment Leasing Platform | Portfolio Project by Matthew David Scott
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
