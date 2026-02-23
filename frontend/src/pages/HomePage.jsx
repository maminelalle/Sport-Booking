import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MapPin, Calendar, ChevronRight, Star, Loader } from 'lucide-react';
import Navbar from '../components/Navbar';
import { useCourts } from '../hooks/useDynamicData';

export default function HomePage() {
  const [sport, setSport] = useState('Football');
  const [location, setLocation] = useState('');
  const [date, setDate] = useState('');
  const navigate = useNavigate();
  const { courts, loading, error } = useCourts();

  // Ensure courts is always an array
  const courtsArray = Array.isArray(courts) ? courts : [];

  // Get featured courts (first 6)
  const featuredCourts = courtsArray.slice(0, 6);

  // Get unique sports and locations
  const uniqueSports = [...new Set(courtsArray.map(court => court.sport_type))];
  const uniqueLocations = [...new Set(courtsArray.map(court => court.site?.name || 'Unknown'))];

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

      {/* Hero Section */}
      <div 
        className="relative bg-gradient-to-r from-blue-600 to-blue-700 py-16 lg:py-20"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center">
            {/* Left: Text Content */}
            <div className="text-white z-10">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
                Réservez facilement votre<br />
                <span className="text-blue-100">terrain de sport</span>
              </h1>
              <p className="text-lg md:text-xl text-blue-100 mb-8">
                Trouvez et réservez les meilleurs terrains de sport près de chez vous en quelques clics
              </p>
              <button 
                onClick={() => navigate('/search')}
                className="bg-white text-blue-600 font-bold py-3 px-8 rounded-lg hover:bg-blue-50 transition shadow-lg"
              >
                Commencer la recherche
              </button>
            </div>

            {/* Right: Football Field Image/Illustration */}
            <div className="relative h-80 md:h-96 lg:h-full">
              <div className="absolute inset-0 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl shadow-2xl overflow-hidden">
                {/* Football Field SVG */}
                <svg
                  viewBox="0 0 400 600"
                  className="w-full h-full"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  {/* Field background */}
                  <rect width="400" height="600" fill="#2d5a2d" />
                  
                  {/* Field lines */}
                  <line x1="200" y1="0" x2="200" y2="600" stroke="white" strokeWidth="3" />
                  <circle cx="200" cy="300" r="50" fill="none" stroke="white" strokeWidth="2" />
                  <circle cx="200" cy="300" r="5" fill="white" />
                  
                  {/* Goal areas */}
                  <rect x="100" y="0" width="200" height="80" fill="none" stroke="white" strokeWidth="2" />
                  <rect x="100" y="520" width="200" height="80" fill="none" stroke="white" strokeWidth="2" />
                  
                  {/* Penalty boxes */}
                  <rect x="130" y="0" width="140" height="120" fill="none" stroke="white" strokeWidth="2" />
                  <rect x="130" y="480" width="140" height="120" fill="none" stroke="white" strokeWidth="2" />
                  
                  {/* Goal lines */}
                  <line x1="0" y1="0" x2="400" y2="0" stroke="white" strokeWidth="3" />
                  <line x1="0" y1="600" x2="400" y2="600" stroke="white" strokeWidth="3" />
                  
                  {/* Side lines */}
                  <line x1="0" y1="0" x2="0" y2="600" stroke="white" strokeWidth="3" />
                  <line x1="400" y1="0" x2="400" y2="600" stroke="white" strokeWidth="3" />
                  
                  {/* Corners */}
                  <circle cx="0" cy="0" r="20" fill="none" stroke="white" strokeWidth="2" />
                  <circle cx="400" cy="0" r="20" fill="none" stroke="white" strokeWidth="2" />
                  <circle cx="0" cy="600" r="20" fill="none" stroke="white" strokeWidth="2" />
                  <circle cx="400" cy="600" r="20" fill="none" stroke="white" strokeWidth="2" />
                </svg>
              </div>
              
              {/* Decorative elements */}
              <div className="absolute -top-10 -right-10 w-40 h-40 bg-blue-400 rounded-full opacity-20"></div>
              <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-blue-300 rounded-full opacity-20"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      <div className="max-w-6xl mx-auto px-4 -mt-16 relative z-20 mb-12">
        <div className="bg-white rounded-2xl shadow-lg p-6 md:p-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Sport Dropdown */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Sport</label>
              <select 
                value={sport}
                onChange={(e) => setSport(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {uniqueSports.length > 0 ? (
                  uniqueSports.map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))
                ) : (
                  <option>Football</option>
                )}
              </select>
            </div>

            {/* Location */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-3.5 text-gray-400" size={20} />
                <select
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Locations</option>
                  {uniqueLocations.map(l => (
                    <option key={l} value={l}>{l}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Date</label>
              <div className="relative">
                <Calendar className="absolute left-3 top-3.5 text-gray-400" size={20} />
                <input 
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Search Button */}
            <div className="flex items-end">
              <button 
                onClick={() => navigate('/search')}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold py-3 rounded-xl hover:from-blue-700 hover:to-blue-800 transition shadow-lg"
              >
                Search
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          {[
            { icon: '🏟️', label: 'Total Courts', value: courtsArray.length + '+' },
            { icon: '📍', label: 'Cities', value: uniqueLocations.length + '+' },
            { icon: '⚽', label: 'Sports', value: uniqueSports.length + '' },
            { icon: '⭐', label: 'Avg Rating', value: '4.8' },
          ].map((stat, idx) => (
            <div key={idx} className="bg-white rounded-2xl shadow-sm p-6 text-center hover:shadow-md transition">
              <div className="text-4xl mb-2">{stat.icon}</div>
              <p className="text-gray-600 text-sm font-medium">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Popular Sports Venues */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Popular Sports Venues</h2>
            <Link to="/search" className="flex items-center text-blue-600 hover:text-blue-700 font-semibold">
              View All <ChevronRight size={20} />
            </Link>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <Loader className="animate-spin text-blue-600" size={32} />
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-700">
              <p>Error loading courts: {error}</p>
            </div>
          ) : featuredCourts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {featuredCourts.map((court) => (
                <div key={court.id} className="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition duration-300 transform hover:scale-105">
                  {/* Image with sport color background */}
                  <div 
                    className="h-48 relative flex items-center justify-center text-white text-4xl font-bold"
                    style={{ backgroundColor: getBackgroundColor(court.sport_type) }}
                  >
                    🏟️
                    <div className="absolute top-4 right-4 bg-white rounded-full px-3 py-1 flex items-center space-x-1 shadow-lg">
                      <Star size={16} className="text-yellow-400 fill-yellow-400" />
                      <span className="font-semibold text-gray-900">4.8</span>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-1">{court.name}</h3>
                    <p className="text-gray-600 text-sm mb-2 flex items-center">
                      <MapPin size={16} className="mr-1" /> {court.site?.name || 'Unknown'}
                    </p>
                    <p className="text-gray-500 text-xs mb-4">Capacity: {court.capacity} persons</p>

                    {/* Sports Tags */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
                        {court.sport_type}
                      </span>
                    </div>

                    {/* Price and Button */}
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-600 text-sm">From</p>
                        <p className="text-2xl font-bold text-gray-900">{court.price_per_hour}<span className="text-sm text-gray-600">/hr</span></p>
                      </div>
                      <button 
                        onClick={() => navigate(`/court/${court.id}`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition shadow-md"
                      >
                        Book Now
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No courts available</p>
            </div>
          )}
        </div>

        {/* How It Works */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 md:p-12">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">How It Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { step: '1', title: 'Search', desc: 'Find courts by location and sport' },
              { step: '2', title: 'Select', desc: 'Choose date and time' },
              { step: '3', title: 'Pay', desc: 'Secure payment online' },
              { step: '4', title: 'Enjoy', desc: 'Play your favorite sport' },
            ].map((item, idx) => (
              <div key={idx} className="text-center">
                <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-20">
        <div className="max-w-6xl mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="font-bold mb-4">About</h4>
              <ul className="space-y-2 text-gray-400">
                <li><span className="hover:text-white transition cursor-pointer">About Us</span></li>
                <li><span className="hover:text-white transition cursor-pointer">Blog</span></li>
                <li><span className="hover:text-white transition cursor-pointer">Careers</span></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><span className="hover:text-white transition cursor-pointer">Help Center</span></li>
                <li><span className="hover:text-white transition cursor-pointer">Contact</span></li>
                <li><span className="hover:text-white transition cursor-pointer">FAQ</span></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><span className="hover:text-white transition cursor-pointer">Privacy</span></li>
                <li><span className="hover:text-white transition cursor-pointer">Terms</span></li>
                <li><span className="hover:text-white transition cursor-pointer">Cookies</span></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Follow Us</h4>
              <div className="flex space-x-4">
                <span className="text-gray-400 hover:text-white transition cursor-pointer">Twitter</span>
                <span className="text-gray-400 hover:text-white transition cursor-pointer">Instagram</span>
                <span className="text-gray-400 hover:text-white transition cursor-pointer">Facebook</span>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-700 pt-8 text-center text-gray-400">
            <p>&copy; 2024 SportBook. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
