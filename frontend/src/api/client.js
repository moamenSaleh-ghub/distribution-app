// API client configuration
// This will be set from environment variable or default to local development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001'

export const apiClient = {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body)
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Request failed')
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

