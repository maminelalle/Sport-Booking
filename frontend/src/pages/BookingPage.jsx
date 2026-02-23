import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ChevronLeft, Calendar, Clock, Check, MapPin, Loader, AlertCircle } from 'lucide-react';
import Navbar from '../components/Navbar';
import { useCourtDetail } from '../hooks/useDynamicData';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export default function BookingPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { court, loading: courtLoading } = useCourtDetail(id);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  
  const [bookingData, setBookingData] = useState({
    date: '',
    start_time: '09:00',
    end_time: '10:00',
    notes: '',
  });

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const calculateDuration = () => {
    if (!bookingData.start_time || !bookingData.end_time) return 0;
    const start = new Date(`2000-01-01T${bookingData.start_time}`);
    const end = new Date(`2000-01-01T${bookingData.end_time}`);
    return (end - start) / (1000 * 60 * 60);
  };

  const calculateTotal = () => {
    const duration = calculateDuration();
    const courtPrice = parseFloat(court?.price_per_hour || 0) * duration;
    const serviceFee = courtPrice * 0.1;
    return { courtPrice, serviceFee, total: courtPrice + serviceFee };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!bookingData.date || !bookingData.start_time || !bookingData.end_time) {
      setError('Veuillez remplir tous les champs obligatoires');
      return;
    }

    const duration = calculateDuration();
    if (duration <= 0) {
      setError('L\'heure de fin doit être après l\'heure de début');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const userEmail = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')).email : null;
      
      if (!userEmail) {
        setError('Email utilisateur non trouvé. Veuillez vous reconnecter.');
        navigate('/login');
        return;
      }

      console.log('✅ User email found:', userEmail);

      // Formater les dates pour l'API Django
      const startDateTime = `${bookingData.date}T${bookingData.start_time}:00`;
      const endDateTime = `${bookingData.date}T${bookingData.end_time}:00`;

      const payload = {
        court: parseInt(id),
        start_datetime: startDateTime,
        end_datetime: endDateTime,
        notes: bookingData.notes || 'Paiement sur place',
        user_email: userEmail,
      };

      console.log('📤 Sending request to:', `${API_BASE_URL}/reservations/`);
      console.log('📦 Payload:', payload);

      const response = await fetch(`${API_BASE_URL}/reservations/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      console.log('📥 Response status:', response.status);
      
      const data = await response.json();
      console.log('📥 Response data:', data);

      if (!response.ok) {
        throw new Error(data.detail || data.error || 'Erreur lors de la réservation');
      }

      console.log('✅ Reservation created successfully');
      setSuccess(true);
      setTimeout(() => {
        navigate('/my-reservations');
      }, 2000);
    } catch (error) {
      console.error('❌ Booking error:', error);
      setError(error.message || 'Une erreur s\'est produite lors de la réservation');
    } finally {
      setLoading(false);
    }
  };

  const timeSlots = Array.from({ length: 15 }, (_, i) => {
    const hour = 8 + i;
    return `${hour.toString().padStart(2, '0')}:00`;
  });

  if (courtLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-96">
          <Loader className="animate-spin text-blue-600" size={48} />
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-2xl mx-auto px-4 py-16">
          <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <Check className="text-green-600" size={40} />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Réservation Confirmée !</h2>
            <p className="text-gray-600 mb-4">
              Votre réservation a été enregistrée avec succès.
            </p>
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-6 text-left">
              <p className="text-yellow-800 text-sm">
                <strong>💵 Paiement sur place:</strong> {calculateTotal().total.toFixed(2)} MRU à payer lors de votre arrivée
              </p>
              <p className="text-yellow-700 text-xs mt-2">
                Veuillez arriver 10 minutes en avance pour effectuer le paiement.
              </p>
            </div>
            <button
              onClick={() => navigate('/my-reservations')}
              className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              Voir mes réservations
            </button>
          </div>
        </div>
      </div>
    );
  }

  const { courtPrice, serviceFee, total } = calculateTotal();

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-6xl mx-auto px-4 py-8">
        <button 
          onClick={() => navigate(`/court/${id}`)}
          className="flex items-center text-blue-600 hover:text-blue-700 font-semibold mb-8 transition"
        >
          <ChevronLeft size={20} />
          Retour aux détails
        </button>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <p className="text-red-800 font-semibold">Erreur</p>
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Résumé à gauche */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Résumé</h2>

            <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl p-6 mb-6">
              <h3 className="text-xl font-bold text-gray-900 mb-2">{court?.name}</h3>
              <p className="text-gray-700 text-sm flex items-start gap-2 mb-2">
                <MapPin size={16} className="mt-1 flex-shrink-0" />
                {court?.site?.name}
              </p>
              <div className="flex gap-2 mt-3">
                <span className="px-3 py-1 bg-white rounded-full text-sm font-medium text-blue-600">
                  {court?.sport_type}
                </span>
                <span className="px-3 py-1 bg-white rounded-full text-sm font-medium text-gray-700">
                  Capacité: {court?.capacity}
                </span>
              </div>
            </div>

            {bookingData.date && (
              <div className="space-y-3 mb-6">
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2 text-gray-700">
                    <Calendar size={18} />
                    <span>Date</span>
                  </div>
                  <span className="font-semibold text-gray-900">
                    {new Date(bookingData.date + 'T00:00').toLocaleDateString('fr-FR')}
                  </span>
                </div>

                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2 text-gray-700">
                    <Clock size={18} />
                    <span>Horaire</span>
                  </div>
                  <span className="font-semibold text-gray-900">
                    {bookingData.start_time} - {bookingData.end_time}
                  </span>
                </div>

                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2 text-gray-700">
                    <Clock size={18} />
                    <span>Durée</span>
                  </div>
                  <span className="font-semibold text-gray-900">
                    {calculateDuration()}h
                  </span>
                </div>
              </div>
            )}

            {calculateDuration() > 0 && (
              <>
                <hr className="my-6" />
                <div className="space-y-3">
                  <div className="flex justify-between text-gray-700">
                    <span>Location terrain ({calculateDuration()}h)</span>
                    <span className="font-semibold">{courtPrice.toFixed(2)} MRU</span>
                  </div>
                  <div className="flex justify-between text-gray-700">
                    <span>Frais de service (10%)</span>
                    <span className="font-semibold">{serviceFee.toFixed(2)} MRU</span>
                  </div>
                  <div className="border-t pt-3 flex justify-between">
                    <span className="text-lg font-bold text-gray-900">Total à payer</span>
                    <span className="text-2xl font-bold text-blue-600">{total.toFixed(2)} MRU</span>
                  </div>
                </div>

                <div className="mt-6 bg-blue-50 border border-blue-200 rounded-xl p-4">
                  <p className="text-blue-800 text-sm">
                    <strong>💵 Paiement sur place</strong><br/>
                    Vous paierez ce montant directement au site sportif lors de votre arrivée.
                  </p>
                </div>
              </>
            )}
          </div>

          {/* Formulaire à droite */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Réserver maintenant</h2>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Date <span className="text-red-500">*</span>
                </label>
                <input
                  type="date"
                  value={bookingData.date}
                  onChange={(e) => setBookingData({ ...bookingData, date: e.target.value })}
                  min={new Date().toISOString().split('T')[0]}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Heure début <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={bookingData.start_time}
                    onChange={(e) => setBookingData({ ...bookingData, start_time: e.target.value })}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {timeSlots.map(time => (
                      <option key={time} value={time}>{time}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Heure fin <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={bookingData.end_time}
                    onChange={(e) => setBookingData({ ...bookingData, end_time: e.target.value })}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {timeSlots.map(time => (
                      <option key={time} value={time}>{time}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Notes (Optionnel)
                </label>
                <textarea
                  value={bookingData.notes}
                  onChange={(e) => setBookingData({ ...bookingData, notes: e.target.value })}
                  rows="4"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Demandes spéciales, nombre de joueurs, etc..."
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader className="animate-spin" size={20} />
                    Réservation en cours...
                  </>
                ) : (
                  <>
                    <Check size={20} />
                    Confirmer la réservation
                  </>
                )}
              </button>

              <p className="text-xs text-gray-500 text-center">
                En réservant, vous acceptez nos conditions d'utilisation. 
                Annulation gratuite jusqu'à 24h avant.
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
