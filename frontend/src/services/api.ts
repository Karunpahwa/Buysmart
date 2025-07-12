import axios from 'axios'

// Use environment variable for API base URL, fallback to relative path for Vercel
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authApi = {
  login: async (email: string, password: string) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  register: async (email: string, password: string) => {
    const response = await api.post('/auth/register', {
      email,
      password,
    })
    return response.data
  },

  getCurrentUser: async (token: string) => {
    const response = await api.get('/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return response.data
  },
}

// Requirements API
export const requirementsApi = {
  getRequirements: async (skip = 0, limit = 100) => {
    const response = await api.get('/requirements', {
      params: { skip, limit },
    })
    return response.data
  },

  getRequirement: async (id: string) => {
    const response = await api.get(`/requirements/${id}`)
    return response.data
  },

  createRequirement: async (data: any) => {
    const response = await api.post('/requirements', data)
    return response.data
  },

  updateRequirement: async (id: string, data: any) => {
    const response = await api.patch(`/requirements/${id}`, data)
    return response.data
  },

  deleteRequirement: async (id: string) => {
    const response = await api.delete(`/requirements/${id}`)
    return response.data
  },
}

// Listings API
export const listingsApi = {
  getListings: async (requirementId: string) => {
    const response = await api.get(`/listings/${requirementId}`)
    return response.data
  },

  getListing: async (listingId: string) => {
    const response = await api.get(`/listings/item/${listingId}`)
    return response.data
  },

  createListing: async (data: any) => {
    const response = await api.post('/listings/', data)
    return response.data
  },

  updateListing: async (listingId: string, data: any) => {
    const response = await api.patch(`/listings/item/${listingId}`, data)
    return response.data
  },

  deleteListing: async (listingId: string) => {
    const response = await api.delete(`/listings/item/${listingId}`)
    return response.data
  },
}

// Messages API
export const messagesApi = {
  getMessages: async (listingId: string) => {
    const response = await api.get(`/messages/${listingId}`)
    return response.data
  },

  sendMessage: async (listingId: string, data: any) => {
    const response = await api.post(`/messages/${listingId}`, data)
    return response.data
  },
}

export default api 