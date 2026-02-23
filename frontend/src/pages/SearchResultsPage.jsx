import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Star, Filter, Loader } from 'lucide-react';
import Navbar from '../components/Navbar';
import { useCourts } from '../hooks/useDynamicData';

export default function SearchResultsPage() {
  const navigate = useNavigate();
  const { courts, loading, error } = useCourts();
  
  const [filters, setFilters] = useState({
    sport: '',
    location: '',
    priceRange: 'all',
    sortBy: 'popular'
  });

  // Ensure courts is always an array
  const courtsArray = Array.isArray(courts) ? courts : [];

  // Get unique sports and locations
  const uniqueSports = [...new Set(courtsArray.map(court => court.sport_type))];
  const uniqueLocations = [...new Set(courtsArray.map(court => court.site?.name || 'Unknown'))];

  // Filter courts based on filters
  const filteredCourts = courtsArray.filter(court => {
    if (filters.sport && court.sport_type !== filters.sport) return false;
    if (filters.location && court.site?.name !== filters.location) return false;
    if (filters.priceRange === 'low' && court.price_per_hour > 60) return false;
    if (filters.priceRange === 'medium' && (court.price_per_hour < 60 || court.price_per_hour > 70)) return false;
    if (filters.priceRange === 'high' && court.price_per_hour < 70) return false;
    return true;
  });

  // Sort courts
  const sortedCourts = [...filteredCourts].sort((a, b) => {
    if (filters.sortBy === 'price-low') return a.price_per_hour - b.price_per_hour;
    if (filters.sortBy === 'price-high') return b.price_per_hour - a.price_per_hour;
    return 0; // popular by default
  });

  const colorMap = {
    'Football': '#3B82F6',
    'Tennis': '#10B981',
    'Basketball': '#F59E0B',
    'Volleyball': '#EF4444',
    'Rugby': '#8B5CF6',
  };

  const getBackgroundColor = (sportType) => {
    return colorMap[sportType] || '#6B7280';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Find Your Perfect Court</h1>
          <p className="text-gray-600">Browse through {courtsArray.length} available sports venues</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Filters */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-md p-6 sticky top-4">
              <div className="flex items-center mb-6">
                <Filter size={20} className="mr-2 text-blue-600" />
                <h2 className="text-lg font-bold text-gray-900">Filters</h2>
              </div>

              {/* Sport Filter */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Sport Type</label>
                <select
                  value={filters.sport}
                  onChange={(e) => setFilters({ ...filters, sport: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Sports</option>
                  {uniqueSports.map(sport => (
                    <option key={sport} value={sport}>{sport}</option>
                  ))}
                </select>
              </div>

              {/* Location Filter */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Location</label>
                <select
                  value={filters.location}
                  onChange={(e) => setFilters({ ...filters, location: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Locations</option>
                  {uniqueLocations.map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>

              {/* Price Range */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Price Range</label>
                <select
                  value={filters.priceRange}
                  onChange={(e) => setFilters({ ...filters, priceRange: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">All Prices</option>
                  <option value="low">Under 60 MRU/hr</option>
                  <option value="medium">60-70 MRU/hr</option>
                  <option value="high">70+ MRU/hr</option>
                </select>
              </div>

              {/* Sort By */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Sort By</label>
                <select
                  value={filters.sortBy}
                  onChange={(e) => setFilters({ ...filters, sortBy: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="popular">Most Popular</option>
                  <option value="price-low">Price: Low to High</option>
                  <option value="price-high">Price: High to Low</option>
                </select>
              </div>

              {/* Reset Filters */}
              <button
                onClick={() => setFilters({ sport: '', location: '', priceRange: 'all', sortBy: 'popular' })}
                className="w-full bg-gray-100 text-gray-700 font-semibold py-2 rounded-lg hover:bg-gray-200 transition"
              >
                Reset Filters
              </button>
            </div>
          </div>

          {/* Results Grid */}
          <div className="lg:col-span-3">
            {/* Results Count */}
            <div className="mb-6">
              <p className="text-gray-600">
                Showing <span className="font-semibold text-gray-900">{sortedCourts.length}</span> results
              </p>
            </div>

            {loading ? (
              <div className="flex justify-center items-center h-64">
                <Loader className="animate-spin text-blue-600" size={32} />
              </div>
            ) : error ? (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-700">
                <p>Error loading courts: {error}</p>
              </div>
            ) : sortedCourts.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {sortedCourts.map((court) => (
                  <div
                    key={court.id}
                    className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition duration-300 cursor-pointer"
                    onClick={() => navigate(`/court/${court.id}`)}
                  >
                    {/* Image */}
                    <div
                      className="h-40 relative flex items-center justify-center text-white text-3xl"
                      style={{ backgroundColor: getBackgroundColor(court.sport_type) }}
                    >
                      🏟️
                      <div className="absolute top-3 right-3 bg-white rounded-full px-2 py-1 flex items-center space-x-1 shadow-md">
                        <Star size={14} className="text-yellow-400 fill-yellow-400" />
                        <span className="text-xs font-semibold text-gray-900">4.8</span>
                      </div>
                    </div>

                    {/* Content */}
                    <div className="p-4">
                      <h3 className="text-lg font-bold text-gray-900 mb-1 line-clamp-1">{court.name}</h3>
                      <p className="text-gray-600 text-sm mb-2 flex items-center">
                        <MapPin size={14} className="mr-1" />
                        {court.site?.name || 'Unknown'}
                      </p>

                      {/* Sport Tag */}
                      <div className="mb-3">
                        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">
                          {court.sport_type}
                        </span>
                      </div>

                      {/* Price */}
                      <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                        <div>
                          <p className="text-xs text-gray-500">From</p>
                          <p className="text-xl font-bold text-gray-900">
                            {court.price_per_hour}<span className="text-sm text-gray-600">/hr</span>
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/court/${court.id}`);
                          }}
                          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition text-sm"
                        >
                          View Details
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No courts found matching your criteria</p>
                <button
                  onClick={() => setFilters({ sport: '', location: '', priceRange: 'all', sortBy: 'popular' })}
                  className="mt-4 text-blue-600 hover:text-blue-700 font-semibold"
                >
                  Reset Filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
