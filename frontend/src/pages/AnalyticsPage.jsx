import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  TrendingUp, Calendar, Clock, DollarSign, 
  PieChart, BarChart3, Activity, Award 
} from 'lucide-react';
import Navbar from '../components/Navbar';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export default function AnalyticsPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalReservations: 0,
    totalSpent: 0,
    hoursBooked: 0,
    favoriteSport: 'Football',
    upcomingBookings: 0,
    cancelledBookings: 0,
  });
  const [reservations, setReservations] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }
    fetchAnalytics();
  }, [navigate]);

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      // Fetch reservations
      const resResponse = await fetch(`${API_BASE_URL}/reservations/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (resResponse.ok) {
        const resData = await resResponse.json();
        const reservationsList = Array.isArray(resData) ? resData : resData.results || [];
        setReservations(reservationsList);

        // Calculate statistics
        const total = reservationsList.length;
        const totalAmount = reservationsList.reduce((sum, r) => {
          return sum + parseFloat(r.total_price || 0);
        }, 0);

        const totalHours = reservationsList.reduce((sum, r) => {
          if (r.start_time && r.end_time) {
            const start = new Date(`2000-01-01T${r.start_time}`);
            const end = new Date(`2000-01-01T${r.end_time}`);
            const hours = (end - start) / (1000 * 60 * 60);
            return sum + hours;
          }
          return sum;
        }, 0);

        const upcoming = reservationsList.filter(r => {
          const resDate = new Date(r.date);
          return resDate > new Date() && r.status === 'CONFIRMED';
        }).length;

        const cancelled = reservationsList.filter(r => r.status === 'CANCELLED').length;

        // Find favorite sport
        const sportCounts = {};
        reservationsList.forEach(r => {
          const sport = r.court?.sport_type || 'Other';
          sportCounts[sport] = (sportCounts[sport] || 0) + 1;
        });
        const favSport = Object.keys(sportCounts).reduce((a, b) => 
          sportCounts[a] > sportCounts[b] ? a : b, 'Football'
        );

        // Monthly data for chart
        const monthlyStats = Array(6).fill(0).map((_, i) => {
          const date = new Date();
          date.setMonth(date.getMonth() - (5 - i));
          const month = date.toLocaleDateString('en-US', { month: 'short' });
          
          const count = reservationsList.filter(r => {
            const resDate = new Date(r.date);
            return resDate.getMonth() === date.getMonth() && 
                   resDate.getFullYear() === date.getFullYear();
          }).length;

          return { month, count };
        });

        setStats({
          totalReservations: total,
          totalSpent: totalAmount,
          hoursBooked: totalHours,
          favoriteSport: favSport,
          upcomingBookings: upcoming,
          cancelledBookings: cancelled,
        });

        setMonthlyData(monthlyStats);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const maxCount = Math.max(...monthlyData.map(d => d.count), 1);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-2 text-gray-600">Track your booking activity and statistics</p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Bookings</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">
                      {stats.totalReservations}
                    </p>
                    <p className="text-xs text-green-600 mt-1 flex items-center gap-1">
                      <TrendingUp size={14} />
                      All time
                    </p>
                  </div>
                  <div className="bg-blue-100 p-4 rounded-full">
                    <Calendar className="text-blue-600" size={28} />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Spent</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">
                      {stats.totalSpent.toFixed(0)}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">MRU</p>
                  </div>
                  <div className="bg-green-100 p-4 rounded-full">
                    <DollarSign className="text-green-600" size={28} />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Hours Booked</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">
                      {stats.hoursBooked.toFixed(1)}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">hours</p>
                  </div>
                  <div className="bg-purple-100 p-4 rounded-full">
                    <Clock className="text-purple-600" size={28} />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Favorite Sport</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">
                      {stats.favoriteSport}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">most played</p>
                  </div>
                  <div className="bg-yellow-100 p-4 rounded-full">
                    <Award className="text-yellow-600" size={28} />
                  </div>
                </div>
              </div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              {/* Monthly Bookings Chart */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center gap-2 mb-6">
                  <BarChart3 className="text-blue-600" size={24} />
                  <h2 className="text-xl font-bold text-gray-900">Monthly Bookings</h2>
                </div>
                <div className="space-y-4">
                  {monthlyData.map((data, index) => (
                    <div key={index}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">{data.month}</span>
                        <span className="text-sm font-bold text-gray-900">{data.count}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                          className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${(data.count / maxCount) * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Activity Summary */}
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center gap-2 mb-6">
                  <Activity className="text-green-600" size={24} />
                  <h2 className="text-xl font-bold text-gray-900">Activity Summary</h2>
                </div>
                <div className="space-y-4">
                  <div className="p-4 bg-green-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-700">Upcoming Bookings</span>
                      <span className="text-2xl font-bold text-green-600">{stats.upcomingBookings}</span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">Active reservations</p>
                  </div>

                  <div className="p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-700">Completed</span>
                      <span className="text-2xl font-bold text-blue-600">
                        {stats.totalReservations - stats.upcomingBookings - stats.cancelledBookings}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">Past bookings</p>
                  </div>

                  <div className="p-4 bg-red-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-700">Cancelled</span>
                      <span className="text-2xl font-bold text-red-600">{stats.cancelledBookings}</span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">Cancelled bookings</p>
                  </div>

                  <div className="p-4 bg-purple-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-700">Avg. Booking Value</span>
                      <span className="text-2xl font-bold text-purple-600">
                        {stats.totalReservations > 0 ? (stats.totalSpent / stats.totalReservations).toFixed(0) : 0}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">MRU per booking</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Insights */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center gap-2 mb-6">
                <PieChart className="text-purple-600" size={24} />
                <h2 className="text-xl font-bold text-gray-900">Insights</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 border-l-4 border-blue-600 bg-blue-50 rounded">
                  <h3 className="font-semibold text-gray-900 mb-1">Most Active Day</h3>
                  <p className="text-sm text-gray-600">
                    You book most frequently on weekends
                  </p>
                </div>
                <div className="p-4 border-l-4 border-green-600 bg-green-50 rounded">
                  <h3 className="font-semibold text-gray-900 mb-1">Preferred Time</h3>
                  <p className="text-sm text-gray-600">
                    Evening slots (18:00 - 20:00) are your favorite
                  </p>
                </div>
                <div className="p-4 border-l-4 border-purple-600 bg-purple-50 rounded">
                  <h3 className="font-semibold text-gray-900 mb-1">Booking Pattern</h3>
                  <p className="text-sm text-gray-600">
                    You typically book 2-3 days in advance
                  </p>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
