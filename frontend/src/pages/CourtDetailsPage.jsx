import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Star, MapPin, Users, Wifi, Navigation, Zap, Calendar, ChevronLeft, ChevronRight, Loader } from 'lucide-react';
import Navbar from '../components/Navbar';
import { useCourtDetail } from '../hooks/useDynamicData';

export default function CourtDetailsPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { court, loading, error } = useCourtDetail(id);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');

  const amenities = [
    { icon: Wifi, name: 'WiFi' },
    { icon: Navigation, name: 'Parking' },
    { icon: Zap, name: 'Lighting' },
    { icon: Users, name: 'Locker Rooms' },
  ];

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

  const images = court ? [
    getBackgroundColor(court.sport_type),
    getBackgroundColor(court.sport_type),
    getBackgroundColor(court.sport_type),
  ] : [];

  const timeSlots = ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM'];

  const nextImage = () => {
    setSelectedImageIndex((prev) => (prev + 1) % images.length);
  };

  const prevImage = () => {
    setSelectedImageIndex((prev) => (prev - 1 + images.length) % images.length);
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

  if (error || !court) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-700">
            <p>{error || 'Court not found'}</p>
            <button
              onClick={() => navigate('/search')}
              className="mt-4 text-blue-600 hover:text-blue-700 font-semibold"
            >
              Return to Search
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Court Details */}
          <div className="lg:col-span-2">
            {/* Image Gallery */}
            <div className="bg-white rounded-2xl overflow-hidden shadow-lg mb-8">
              <div 
                className="h-96 relative flex items-center justify-center text-white text-6xl"
                style={{ backgroundColor: images[selectedImageIndex] }}
              >
                🏟️
                
                {/* Image Navigation */}
                <button
                  onClick={prevImage}
                  className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition"
                >
                  <ChevronLeft size={24} className="text-gray-900" />
                </button>

                <button
                  onClick={nextImage}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition"
                >
                  <ChevronRight size={24} className="text-gray-900" />
                </button>

                {/* Image counter */}
                <div className="absolute bottom-4 right-4 bg-black/60 text-white px-3 py-1 rounded-lg text-sm font-semibold">
                  {selectedImageIndex + 1} / {images.length}
                </div>
              </div>

              {/* Thumbnail Gallery */}
              <div className="flex gap-2 p-4">
                {images.map((color, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedImageIndex(idx)}
                    className={`w-20 h-20 rounded-lg overflow-hidden border-2 transition flex items-center justify-center ${
                      selectedImageIndex === idx ? 'border-blue-600' : 'border-gray-200'
                    }`}
                    style={{ backgroundColor: color }}
                  >
                    <span className="text-2xl">🏟️</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Court Information */}
            <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-4xl font-bold text-gray-900 mb-2">{court.name}</h1>
                  <p className="text-gray-600 flex items-center mb-4">
                    <MapPin size={20} className="mr-2 text-blue-600" />
                    {court.site?.name || 'Location not specified'}
                  </p>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
                      {court.sport_type}
                    </span>
                    <span className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                      Capacity: {court.capacity} persons
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-1 mb-2">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        size={20}
                        className={i < 4 ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}
                      />
                    ))}
                  </div>
                  <p className="font-semibold text-gray-900">4.8</p>
                  <p className="text-gray-600 text-sm">(125 reviews)</p>
                </div>
              </div>

              {/* Description */}
              <p className="text-gray-700 text-lg mb-8 leading-relaxed">
                {court.description || `Professional ${court.sport_type} court with modern facilities and equipment. Perfect for both casual play and competitive matches. Located at ${court.site?.name || 'a premium sports facility'}.`}
              </p>

              {/* Amenities */}
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Amenities</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {amenities.map((amenity, idx) => {
                    const IconComponent = amenity.icon;
                    return (
                      <div key={idx} className="flex items-center space-x-3 p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition">
                        <IconComponent size={24} className="text-blue-600" />
                        <span className="font-semibold text-gray-900">{amenity.name}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Reviews Section */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-6">Recent Reviews</h3>
              
              <div className="space-y-4">
                {[
                  { name: 'Ahmed M.', rating: 5, text: 'Excellent facility! The courts are well-maintained and the staff is very helpful.' },
                  { name: 'Fatima S.', rating: 4, text: 'Great experience. Clean facilities and good customer service.' },
                  { name: 'Mohamed K.', rating: 5, text: 'Best sports complex in the area. Highly recommended!' },
                ].map((review, idx) => (
                  <div key={idx} className="pb-4 border-b last:border-b-0">
                    <div className="flex items-center justify-between mb-2">
                      <p className="font-semibold text-gray-900">{review.name}</p>
                      <div className="flex space-x-1">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            size={16}
                            className={i < review.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}
                          />
                        ))}
                      </div>
                    </div>
                    <p className="text-gray-600">{review.text}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right: Booking Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-4">
              <div className="mb-6">
                <p className="text-gray-600 text-sm mb-2">Price per hour</p>
                <p className="text-4xl font-bold text-gray-900">
                  {court.price_per_hour}
                  <span className="text-lg text-gray-600"> MRU</span>
                </p>
              </div>

              {/* Date Selection */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  <Calendar size={16} className="inline mr-1" />
                  Select Date
                </label>
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  min={new Date().toISOString().split('T')[0]}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Time Slot Selection */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Select Time Slot</label>
                <div className="grid grid-cols-2 gap-2 max-h-64 overflow-y-auto">
                  {timeSlots.map((slot) => (
                    <button
                      key={slot}
                      onClick={() => setSelectedTime(slot)}
                      className={`py-2 px-3 text-sm rounded-lg border-2 transition ${
                        selectedTime === slot
                          ? 'border-blue-600 bg-blue-50 text-blue-700 font-semibold'
                          : 'border-gray-200 hover:border-blue-300 text-gray-700'
                      }`}
                    >
                      {slot}
                    </button>
                  ))}
                </div>
              </div>

              {/* Booking Summary */}
              {selectedDate && selectedTime && (
                <div className="mb-6 p-4 bg-blue-50 rounded-xl">
                  <p className="text-sm text-gray-600 mb-2">Booking Summary</p>
                  <p className="text-sm font-semibold text-gray-900">{selectedDate}</p>
                  <p className="text-sm font-semibold text-gray-900">{selectedTime}</p>
                  <p className="text-sm text-gray-600 mt-2">Total: <span className="font-bold text-gray-900">{court.price_per_hour} MRU</span></p>
                </div>
              )}

              {/* Book Button */}
              <button
                onClick={() => {
                  if (selectedDate && selectedTime) {
                    navigate(`/booking/${court.id}`, {
                      state: { court, selectedDate, selectedTime }
                    });
                  } else {
                    alert('Please select date and time');
                  }
                }}
                disabled={!selectedDate || !selectedTime}
                className={`w-full py-4 rounded-xl font-bold text-lg transition shadow-lg ${
                  selectedDate && selectedTime
                    ? 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
              >
                Book Now
              </button>

              <p className="text-xs text-gray-500 text-center mt-4">
                Free cancellation up to 24 hours before your booking
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
