import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, MapPin, Clock, DollarSign, CheckCircle, XCircle, Loader, AlertCircle } from 'lucide-react';
import Navbar from '../components/Navbar';
import { useReservations } from '../hooks/useDynamicData';

export default function MyReservationsPage() {
  const navigate = useNavigate();
  const { reservations, loading, error } = useReservations();

  // Check authentication on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login', { state: { message: 'Please login to view your reservations' } });
    }
  }, [navigate]);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'CONFIRMED':
        return <CheckCircle size={20} className="text-green-600" />;
      case 'PENDING':
        return <Clock size={20} className="text-yellow-600" />;
      case 'CANCELLED':
        return <XCircle size={20} className="text-red-600" />;
      default:
        return <AlertCircle size={20} className="text-gray-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'CONFIRMED':
        return 'bg-green-100 text-green-700';
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-700';
      case 'CANCELLED':
        return 'bg-red-100 text-red-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-[60vh]">
          <Loader className="animate-spin text-blue-600" size={48} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">My Reservations</h1>
          <p className="text-gray-600">View and manage your court bookings</p>
        </div>

        {error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-700">
            <p>{error}</p>
          </div>
        ) : reservations.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-md p-12 text-center">
            <Calendar size={64} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-2xl font-bold text-gray-900 mb-2">No Reservations Yet</h3>
            <p className="text-gray-600 mb-6">Start booking your favorite sports venues</p>
            <button
              onClick={() => navigate('/search')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition"
            >
              Browse Courts
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {reservations.map((reservation) => (
              <div
                key={reservation.id}
                className="bg-white rounded-2xl shadow-md hover:shadow-lg transition p-6"
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                  {/* Left: Reservation Info */}
                  <div className="flex-1 mb-4 md:mb-0">
                    <div className="flex items-center mb-2">
                      <h3 className="text-xl font-bold text-gray-900 mr-3">
                        {reservation.court?.name || 'Court Name'}
                      </h3>
                      <span
                        className={`flex items-center space-x-1 text-xs font-semibold px-3 py-1 rounded-full ${getStatusColor(
                          reservation.status
                        )}`}
                      >
                        {getStatusIcon(reservation.status)}
                        <span>{reservation.status}</span>
                      </span>
                    </div>

                    <div className="space-y-2">
                      <p className="text-gray-600 flex items-center">
                        <MapPin size={16} className="mr-2" />
                        {reservation.court?.site?.name || 'Location not specified'}
                      </p>
                      <p className="text-gray-600 flex items-center">
                        <Calendar size={16} className="mr-2" />
                        {formatDate(reservation.start_datetime)}
                      </p>
                      <p className="text-gray-600 flex items-center">
                        <Clock size={16} className="mr-2" />
                        {formatTime(reservation.start_datetime)} - {formatTime(reservation.end_datetime)}
                      </p>
                      <p className="text-gray-600 flex items-center">
                        <DollarSign size={16} className="mr-2" />
                        Total: {reservation.total_price} MRU
                      </p>
                    </div>
                  </div>

                  {/* Right: Actions */}
                  <div className="flex flex-col space-y-2">
                    <button
                      onClick={() => navigate(`/court/${reservation.court?.id}`)}
                      className="px-6 py-2 border-2 border-blue-600 text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition"
                    >
                      View Court
                    </button>
                    {reservation.status === 'CONFIRMED' && (
                      <button className="px-6 py-2 bg-red-100 text-red-700 font-semibold rounded-lg hover:bg-red-200 transition">
                        Cancel
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
