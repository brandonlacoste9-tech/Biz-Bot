import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
// NOTE: For production, consider using httpOnly cookies instead of localStorage
// to protect against XSS attacks. Current implementation is for development ease.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  requestMagicLink: (email: string) => 
    apiClient.post('/api/auth/magic-link/request', { email }),
  
  verifyMagicLink: (token: string) =>
    apiClient.post('/api/auth/magic-link/verify', { token }),
  
  getCurrentUser: () =>
    apiClient.get('/api/auth/me'),
}

// Tenant API
export const tenantAPI = {
  create: (data: any) =>
    apiClient.post('/api/tenants/', data),
  
  get: (id: string) =>
    apiClient.get(`/api/tenants/${id}`),
  
  update: (id: string, data: any) =>
    apiClient.patch(`/api/tenants/${id}`, data),
  
  list: () =>
    apiClient.get('/api/tenants/'),
}

// Booking API
export const bookingAPI = {
  create: (data: any) =>
    apiClient.post('/api/bookings/', data),
  
  list: (params?: any) =>
    apiClient.get('/api/bookings/', { params }),
  
  get: (id: string) =>
    apiClient.get(`/api/bookings/${id}`),
  
  update: (id: string, data: any) =>
    apiClient.patch(`/api/bookings/${id}`, data),
  
  delete: (id: string) =>
    apiClient.delete(`/api/bookings/${id}`),
}

// FAQ API
export const faqAPI = {
  create: (data: any) =>
    apiClient.post('/api/faq/', data),
  
  list: (params?: any) =>
    apiClient.get('/api/faq/', { params }),
  
  search: (query: string, tenantId: string, language: string) =>
    apiClient.get('/api/faq/search', { params: { q: query, tenant_id: tenantId, language } }),
  
  get: (id: string) =>
    apiClient.get(`/api/faq/${id}`),
  
  update: (id: string, data: any) =>
    apiClient.patch(`/api/faq/${id}`, data),
  
  delete: (id: string) =>
    apiClient.delete(`/api/faq/${id}`),
}

// Admin API
export const adminAPI = {
  getStats: () =>
    apiClient.get('/api/admin/stats'),
  
  listUsers: () =>
    apiClient.get('/api/admin/users'),
  
  listTenants: () =>
    apiClient.get('/api/admin/tenants'),
}

export default apiClient
