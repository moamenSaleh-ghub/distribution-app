// API client configuration
// This will be set from environment variable or default to local development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001'

export const apiClient = {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    
    // Get token from localStorage
    const token = localStorage.getItem('authToken')
    
    if (!token) {
      // No token - redirect to login
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
      throw new Error('Not authenticated. Please login.')
    }
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    // Add Authorization header
    config.headers['Authorization'] = `Bearer ${token}`

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body)
    }

    try {
      const response = await fetch(url, config)
      
      // Handle 401 Unauthorized - token invalid or expired
      if (response.status === 401) {
        // Clear token and redirect to login
        localStorage.removeItem('authToken')
        // Only redirect if we're not already on the login page
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login'
        }
        let errorData = {}
        try {
          const text = await response.text()
          errorData = text ? JSON.parse(text) : {}
        } catch (e) {
          // Ignore parse errors
        }
        throw new Error(errorData.message || 'Unauthorized. Please login again.')
      }

      // Parse response as JSON
      let data
      try {
        const text = await response.text()
        data = text ? JSON.parse(text) : {}
      } catch (parseError) {
        console.error('Failed to parse response as JSON:', parseError)
        if (!response.ok) {
          throw new Error(`Server error: ${response.status} ${response.statusText}`)
        }
        throw new Error('Invalid response from server')
      }

      if (!response.ok) {
        throw new Error(data.message || `Request failed: ${response.status} ${response.statusText}`)
      }

      return data
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  },

  get(endpoint, options) {
    return this.request(endpoint, { ...options, method: 'GET' })
  },

  post(endpoint, body, options) {
    return this.request(endpoint, { ...options, method: 'POST', body })
  },

  patch(endpoint, body, options) {
    return this.request(endpoint, { ...options, method: 'PATCH', body })
  },
}

// Products API
export const productsApi = {
  list: (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/products${queryString ? `?${queryString}` : ''}`)
  },
  get: (id) => apiClient.get(`/products/${id}`),
  create: (data) => apiClient.post('/products', data),
  update: (id, data) => apiClient.patch(`/products/${id}`, data),
}

// Customers API
export const customersApi = {
  list: (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/customers${queryString ? `?${queryString}` : ''}`)
  },
  get: (id) => apiClient.get(`/customers/${id}`),
  create: (data) => apiClient.post('/customers', data),
}

// Orders API
export const ordersApi = {
  create: (data) => apiClient.post('/orders', data),
  getCustomerOrders: (customerId, params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/customers/${customerId}/orders${queryString ? `?${queryString}` : ''}`)
  },
}

// Debt API
export const debtApi = {
  adjust: (customerId, data) => apiClient.post(`/customers/${customerId}/adjust-debt`, data),
}

