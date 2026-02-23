import api from './api';

// Authentification
export const authService = {
  register: (data) => api.post('/auth/register/', data),
  login: (email, password) => api.post('/auth/login/', { email, password }),
  logout: () => api.post('/auth/logout/'),
  me: () => api.get('/auth/me/'),
  changePassword: (oldPassword, newPassword) =>
    api.post('/auth/change_password/', { old_password: oldPassword, new_password: newPassword }),
  deleteAccount: (password) => api.post('/auth/delete_account/', { password }),
};

// Sites
export const sitesService = {
  list: (params) => api.get('/sites/', { params }),
  retrieve: (id) => api.get(`/sites/${id}/`),
  create: (data) => api.post('/sites/', data),
  update: (id, data) => api.put(`/sites/${id}/`, data),
  delete: (id) => api.delete(`/sites/${id}/`),
  openingHours: (id) => api.get(`/sites/${id}/opening_hours/`),
  setOpeningHours: (id, data) => api.post(`/sites/${id}/set_opening_hours/`, data),
};

// Terrains
export const courtsService = {
  list: (params) => api.get('/courts/courts/', { params }),
  retrieve: (id) => api.get(`/courts/courts/${id}/`),
  create: (data) => api.post('/courts/courts/', data),
  update: (id, data) => api.put(`/courts/courts/${id}/`, data),
  delete: (id) => api.delete(`/courts/courts/${id}/`),
  checkAvailability: (courtId, start, end) =>
    api.get(`/courts/courts/${courtId}/availability/`, {
      params: { start, end },
    }),
  equipments: () => api.get('/courts/equipments/'),
};

// Réservations
export const reservationsService = {
  list: (params) => api.get('/reservations/', { params }),
  retrieve: (id) => api.get(`/reservations/${id}/`),
  create: (data) => api.post('/reservations/', data),
  myReservations: () => api.get('/reservations/my_reservations/'),
  cancel: (id, reason) => api.post(`/reservations/${id}/cancel/`, { reason }),
  checkAvailability: (data) => api.post('/reservations/check_availability/', data),
  siteStats: (siteId) => api.get('/reservations/site_stats/', { params: { site_id: siteId } }),
};

// Paiements
export const paymentsService = {
  list: (params) => api.get('/payments/payments/', { params }),
  retrieve: (id) => api.get(`/payments/payments/${id}/`),
  createPaymentIntent: (reservationId) =>
    api.post('/payments/payments/create_payment_intent/', { reservation_id: reservationId }),
  confirmPayment: (paymentIntentId) =>
    api.post('/payments/payments/confirm_payment/', { payment_intent_id: paymentIntentId }),
  refund: (id) => api.post(`/payments/payments/${id}/refund/`),
  invoices: () => api.get('/payments/invoices/'),
  downloadInvoice: (id) => api.get(`/payments/invoices/${id}/download/`),
};

export default {
  authService,
  sitesService,
  courtsService,
  reservationsService,
  paymentsService,
};
