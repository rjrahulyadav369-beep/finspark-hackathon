import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (username, email, password, full_name) =>
    api.post('/auth/register', { username, email, password, full_name }),
  getCurrentUser: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
}

export const eventsAPI = {
  getAll: (params) => api.get('/api/events', { params }),
  getById: (id) => api.get(`/api/events/${id}`),
  create: (event) => api.post('/api/events', event),
  getUserEvents: (userId, limit = 50) =>
    api.get(`/api/events/user/${userId}`, { params: { limit } }),
}

export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard/stats'),
  getTimeline: (hours = 24) => api.get('/api/dashboard/timeline', { params: { hours } }),
  getTopUsers: (limit = 10) => api.get('/api/dashboard/top-suspicious-users', { params: { limit } }),
  getRiskDistribution: () => api.get('/api/dashboard/risk-distribution'),
}

export const predictAPI = {
  predictEvent: (event) => api.post('/api/predict/event', event),
  predictBatch: (events) => api.post('/api/predict/batch', events),
  getModelInfo: () => api.get('/api/predict/model/info'),
}

export const usersAPI = {
  getById: (id) => api.get(`/api/users/${id}`),
  getRiskProfile: (id) => api.get(`/api/users/${id}/risk-profile`),
  getTransactions: (id, limit = 50) =>
    api.get(`/api/users/${id}/transaction-history`, { params: { limit } }),
  getLogins: (id, limit = 50) => api.get(`/api/users/${id}/login-history`, { params: { limit } }),
  getDevices: (id) => api.get(`/api/users/${id}/devices`),
}

export const reportsAPI = {
  getSummary: (days = 30) => api.get('/api/reports/summary', { params: { days } }),
  exportCSV: (days = 30) => api.get('/api/reports/export-csv', { params: { days } }),
}

export const chatAPI = {
  ask: (query, userId) => api.post('/api/chat/ask', { query, user_id: userId }),
  explainAlert: (eventId) => api.post('/api/chat/explain-alert', { event_id: eventId }),
}

export default api
