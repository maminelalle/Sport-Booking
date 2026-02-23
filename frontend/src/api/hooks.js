/**
 * Hooks React personnalisés pour l'API
 */

import { useState, useEffect } from 'react';
import { api, API_ENDPOINTS } from './client';

/**
 * Hook pour récupérer une liste de ressources
 */
export const useFetch = (endpoint, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await api.get(endpoint);
        setData(result);
        setError(null);
      } catch (err) {
        setError(err);
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  return { data, loading, error };
};

/**
 * Hook pour effectuer une action (POST, PUT, DELETE)
 */
export const useAction = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = async (method, endpoint, data = null) => {
    try {
      setLoading(true);
      setError(null);
      
      let result;
      switch (method.toLowerCase()) {
        case 'post':
          result = await api.post(endpoint, data);
          break;
        case 'put':
          result = await api.put(endpoint, data);
          break;
        case 'patch':
          result = await api.patch(endpoint, data);
          break;
        case 'delete':
          result = await api.delete(endpoint);
          break;
        default:
          throw new Error(`Unknown method: ${method}`);
      }
      
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
};

/**
 * Hook pour la recherche avec paramètres
 */
export const useSearch = (baseEndpoint) => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = async (params) => {
    try {
      setLoading(true);
      const result = await api.get(baseEndpoint, params);
      setResults(result);
      setError(null);
      return result;
    } catch (err) {
      setError(err);
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  return { results, loading, error, search };
};

/**
 * Hook pour l'authentification
 */
export const useAuth = () => {
  const [user, setUser] = useState(api.getCurrentUser());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const login = async (email, password) => {
    try {
      setLoading(true);
      const data = await api.login(email, password);
      setUser(data.user);
      setError(null);
      return data;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    api.logout();
    setUser(null);
  };

  const isAuthenticated = () => api.isAuthenticated();

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated,
  };
};

/**
 * Hook pour gérer les terrains de sport
 */
export const useCourts = () => {
  const [courts, setCourts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCourts = async (filters = {}) => {
    try {
      setLoading(true);
      const result = await api.get(API_ENDPOINTS.COURTS, filters);
      // Si c'est une pagination
      const courtsList = Array.isArray(result) ? result : result.results;
      setCourts(courtsList);
      setError(null);
      return courtsList;
    } catch (err) {
      setError(err);
      setCourts(null);
    } finally {
      setLoading(false);
    }
  };

  const getCourtDetail = async (id) => {
    try {
      const endpoint = API_ENDPOINTS.COURT_DETAIL.replace('{id}', id);
      return await api.get(endpoint);
    } catch (err) {
      setError(err);
      throw err;
    }
  };

  useEffect(() => {
    fetchCourts();
  }, []);

  return { courts, loading, error, fetchCourts, getCourtDetail };
};

/**
 * Hook pour les réservations
 */
export const useReservations = () => {
  const [reservations, setReservations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReservations = async () => {
    try {
      setLoading(true);
      const result = await api.get(API_ENDPOINTS.RESERVATIONS);
      const reservationsList = Array.isArray(result) ? result : result.results;
      setReservations(reservationsList);
      setError(null);
      return reservationsList;
    } catch (err) {
      setError(err);
      setReservations(null);
    } finally {
      setLoading(false);
    }
  };

  const createReservation = async (data) => {
    try {
      setLoading(true);
      const result = await api.post(API_ENDPOINTS.RESERVATIONS, data);
      setError(null);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateReservation = async (id, data) => {
    try {
      setLoading(true);
      const endpoint = API_ENDPOINTS.RESERVATION_DETAIL.replace('{id}', id);
      const result = await api.put(endpoint, data);
      setError(null);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const cancelReservation = async (id) => {
    try {
      setLoading(true);
      const endpoint = API_ENDPOINTS.RESERVATION_DETAIL.replace('{id}', id);
      const result = await api.delete(endpoint);
      setError(null);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    reservations,
    loading,
    error,
    fetchReservations,
    createReservation,
    updateReservation,
    cancelReservation,
  };
};
