import { useState, useEffect } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Hook personnalisé pour récupérer les sites sportifs
 */
export const useSites = () => {
  const [sites, setSites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSites = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem('access_token');
        const headers = {
          'Content-Type': 'application/json',
        };
        
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}/sites/sites/`, {
          headers,
        });
        
        if (!response.ok) throw new Error('Erreur lors du chargement des sites');
        
        const data = await response.json();
        const sitesData = data.results || data;
        setSites(Array.isArray(sitesData) ? sitesData : []);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Erreur sites:', err);
        setSites([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSites();
  }, []);

  return { sites, loading, error };
};

/**
 * Hook personnalisé pour récupérer les terrains/courts
 */
export const useCourts = () => {
  const [courts, setCourts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourts = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/courts/courts/`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) throw new Error('Erreur lors du chargement des terrains');
        
        const data = await response.json();
        // Ensure we always set an array
        const courtsData = data.results || data;
        setCourts(Array.isArray(courtsData) ? courtsData : []);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Erreur courts:', err);
        setCourts([]); // Set empty array on error
      } finally {
        setLoading(false);
      }
    };

    fetchCourts();
  }, []);

  return { courts, loading, error };
};

/**
 * Hook personnalisé pour récupérer ou chercher les terrains par site ou type de sport
 */
export const useCourtsFiltered = (siteId = null, sportType = null) => {
  const [courts, setCourts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourts = async () => {
      try {
        setLoading(true);
        let url = `${API_BASE_URL}/courts/courts/`;
        
        // Ajouter les paramètres de filtrage
        const params = new URLSearchParams();
        if (siteId) params.append('site_id', siteId);
        if (sportType) params.append('sport_type', sportType);
        
        if (params.toString()) {
          url += `?${params.toString()}`;
        }

        const response = await fetch(url, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) throw new Error('Erreur lors du chargement des terrains');
        
        const data = await response.json();
        const courtsData = data.results || data;
        setCourts(Array.isArray(courtsData) ? courtsData : []);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Erreur courts filtrés:', err);
        setCourts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCourts();
  }, [siteId, sportType]);

  return { courts, loading, error };
};

/**
 * Hook personnalisé pour récupérer les équipements
 */
export const useEquipment = () => {
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEquipment = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/courts/equipments/`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) throw new Error('Erreur lors du chargement des équipements');
        
        const data = await response.json();
        const equipmentData = data.results || data;
        setEquipment(Array.isArray(equipmentData) ? equipmentData : []);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Erreur équipements:', err);
        setEquipment([]);
      } finally {
        setLoading(false);
      }
    };

    fetchEquipment();
  }, []);

  return { equipment, loading, error };
};

/**
 * Hook personnalisé pour récupérer les réservations
 */
export const useReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        setLoading(true);
        const user = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;
        const userEmail = user?.email || '';
        const url = userEmail 
          ? `${API_BASE_URL}/reservations/?user_email=${encodeURIComponent(userEmail)}`
          : `${API_BASE_URL}/reservations/`;

        const response = await fetch(url, {
          headers: { 'Content-Type': 'application/json' },
        });
        
        if (!response.ok) throw new Error('Erreur lors du chargement des réservations');
        
        const data = await response.json();
        const reservationsData = data.results || data;
        setReservations(Array.isArray(reservationsData) ? reservationsData : []);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Erreur réservations:', err);
        setReservations([]);
      } finally {
        setLoading(false);
      }
    };

    fetchReservations();
  }, []);

  return { reservations, loading, error };
};

/**
 * Hook personnalisé pour récupérer un court spécifique par ID
 */
export const useCourtDetail = (courtId) => {
  const [court, setCourt] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!courtId) return;

    const fetchCourt = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/courts/courts/${courtId}/`, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) throw new Error('Erreur lors du chargement du terrain');
        
        const data = await response.json();
        setCourt(data);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Erreur court detail:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCourt();
  }, [courtId]);

  return { court, loading, error };
};

/**
 * Hook personnalisé pour créer une réservation
 */
export const useCreateReservation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const createReservation = async (reservationData) => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      const headers = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}/reservations/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(reservationData),
      });
      
      if (!response.ok) throw new Error('Erreur lors de la création de la réservation');
      
      const data = await response.json();
      setError(null);
      return data;
    } catch (err) {
      setError(err.message);
      console.error('Erreur création réservation:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { createReservation, loading, error };
};
