/**
 * Configuration API pour communiquer avec le backend Django
 */

// URL de base de l'API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Configuration des endpoints API
const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login/',
  LOGOUT: '/auth/logout/',
  REGISTER: '/auth/register/',
  REFRESH_TOKEN: '/auth/refresh/',
  
  // Courts (terrains)
  COURTS: '/courts/courts/',
  COURT_DETAIL: '/courts/courts/{id}/',
  COURT_SEARCH: '/courts/courts/?search=',
  
  // Sites
  SITES: '/sites/',
  SITE_DETAIL: '/sites/{id}/',
  
  // Reservations (réservations)
  RESERVATIONS: '/reservations/',
  RESERVATION_DETAIL: '/reservations/{id}/',
  
  // Payments (paiements)
  PAYMENTS: '/payments/payments/',
  PAYMENT_DETAIL: '/payments/payments/{id}/',
};

/**
 * Classe pour gérer les appels API
 */
class ApiClient {
  constructor() {
    this.token = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  /**
   * Effectue une requête GET
   */
  async get(endpoint, params = {}) {
    return this.request('GET', endpoint, null, params);
  }

  /**
   * Effectue une requête POST
   */
  async post(endpoint, data = {}) {
    return this.request('POST', endpoint, data);
  }

  /**
   * Effectue une requête PUT
   */
  async put(endpoint, data = {}) {
    return this.request('PUT', endpoint, data);
  }

  /**
   * Effectue une requête PATCH
   */
  async patch(endpoint, data = {}) {
    return this.request('PATCH', endpoint, data);
  }

  /**
   * Effectue une requête DELETE
   */
  async delete(endpoint) {
    return this.request('DELETE', endpoint);
  }

  /**
   * Effectue une requête HTTP générique
   */
  async request(method, endpoint, data = null, params = {}) {
    const url = new URL(`${API_BASE_URL}${endpoint}`);

    // Ajouter les paramètres de recherche
    Object.keys(params).forEach((key) => {
      if (params[key]) {
        url.searchParams.append(key, params[key]);
      }
    });

    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    };

    // Ajouter le token d'authentification s'il existe
    if (this.token) {
      options.headers['Authorization'] = `Bearer ${this.token}`;
    }

    // Ajouter les données du corps pour les requêtes non-GET
    if (data && method !== 'GET') {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url.toString(), options);

      // Gérer les erreurs d'authentification
      if (response.status === 401) {
        // Token expiré - essayer de le rafraîchir
        if (this.refreshToken) {
          await this.refreshAccessToken();
          // Relancer la requête avec le nouveau token
          return this.request(method, endpoint, data, params);
        } else {
          // Rediriger vers la connexion
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }

      // Parser la réponse JSON
      const responseData = await response.json().catch(() => null);

      if (!response.ok) {
        const error = new Error(
          responseData?.detail || responseData?.message || 
          `HTTP Error: ${response.status}`
        );
        error.status = response.status;
        error.data = responseData;
        throw error;
      }

      return responseData;
    } catch (error) {
      console.error(`API Error [${method} ${endpoint}]:`, error);
      throw error;
    }
  }

  /**
   * Rafraîchit le token d'accès
   */
  async refreshAccessToken() {
    try {
      const data = await this.request('POST', API_ENDPOINTS.REFRESH_TOKEN, {
        refresh: this.refreshToken,
      });

      if (data.access) {
        this.token = data.access;
        localStorage.setItem('access_token', data.access);
        return true;
      }
    } catch (error) {
      console.error('Failed to refresh token:', error);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return false;
    }
  }

  /**
   * Connexion utilisateur
   */
  async login(email, password) {
    const data = await this.post(API_ENDPOINTS.LOGIN, { email, password });
    if (data.access && data.refresh) {
      this.token = data.access;
      this.refreshToken = data.refresh;
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  }

  /**
   * Déconnexion utilisateur
   */
  logout() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  /**
   * Récupère l'utilisateur connecté
   */
  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  /**
   * Vérifie si l'utilisateur est connecté
   */
  isAuthenticated() {
    return !!this.token;
  }
}

// Export l'instance unique du client API
export const api = new ApiClient();

// Export les endpoints pour utilisation directe
export { API_ENDPOINTS, API_BASE_URL };

// Export la classe pour les tests
export default ApiClient;
