import { describe, it, expect, vi, beforeEach } from 'vitest'
import { apiClient, productsApi, customersApi, ordersApi, debtApi } from '../api/client'

// Mock fetch globally
global.fetch = vi.fn()

describe('API Client', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  describe('apiClient', () => {
    it('should make GET request successfully', async () => {
      const mockResponse = { data: 'test' }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await apiClient.get('/test')

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/test'),
        expect.objectContaining({ method: 'GET' })
      )
      expect(result).toEqual(mockResponse)
    })

    it('should make POST request with body', async () => {
      const mockResponse = { id: '123' }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await apiClient.post('/test', { name: 'Test' })

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/test'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ name: 'Test' }),
        })
      )
      expect(result).toEqual(mockResponse)
    })

    it('should handle errors', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ message: 'Error occurred' }),
      })

      await expect(apiClient.get('/test')).rejects.toThrow()
    })
  })

  describe('productsApi', () => {
    it('should list products', async () => {
      const mockProducts = { items: [{ id: '1', name: 'Product 1' }] }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockProducts,
      })

      const result = await productsApi.list()

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/products'),
        expect.any(Object)
      )
      expect(result).toEqual(mockProducts)
    })

    it('should get single product', async () => {
      const mockProduct = { id: '1', name: 'Product 1' }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      })

      const result = await productsApi.get('1')

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/products/1'),
        expect.any(Object)
      )
      expect(result).toEqual(mockProduct)
    })

    it('should create product', async () => {
      const newProduct = { name: 'New Product', baseBuyingPrice: 10, baseSellingPrice: 15 }
      const mockResponse = { id: '123', ...newProduct }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await productsApi.create(newProduct)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/products'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(newProduct),
        })
      )
      expect(result).toEqual(mockResponse)
    })

    it('should update product', async () => {
      const updates = { name: 'Updated Product' }
      const mockResponse = { id: '1', ...updates }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await productsApi.update('1', updates)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/products/1'),
        expect.objectContaining({
          method: 'PATCH',
          body: JSON.stringify(updates),
        })
      )
      expect(result).toEqual(mockResponse)
    })
  })

  describe('customersApi', () => {
    it('should list customers', async () => {
      const mockCustomers = { items: [{ id: '1', name: 'Customer 1' }] }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockCustomers,
      })

      const result = await customersApi.list()

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/customers'),
        expect.any(Object)
      )
      expect(result).toEqual(mockCustomers)
    })

    it('should create customer', async () => {
      const newCustomer = { name: 'New Customer', location: 'Location', phone: '123' }
      const mockResponse = { id: '123', ...newCustomer }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await customersApi.create(newCustomer)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/customers'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(newCustomer),
        })
      )
      expect(result).toEqual(mockResponse)
    })
  })

  describe('ordersApi', () => {
    it('should create order', async () => {
      const newOrder = { customerId: '1', items: [] }
      const mockResponse = { id: '123', ...newOrder }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await ordersApi.create(newOrder)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/orders'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(newOrder),
        })
      )
      expect(result).toEqual(mockResponse)
    })

    it('should get customer orders', async () => {
      const mockOrders = { items: [{ id: '1' }] }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockOrders,
      })

      const result = await ordersApi.getCustomerOrders('1')

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/customers/1/orders'),
        expect.any(Object)
      )
      expect(result).toEqual(mockOrders)
    })
  })

  describe('debtApi', () => {
    it('should adjust customer debt', async () => {
      const adjustment = { amount: -100, reason: 'Payment' }
      const mockResponse = { id: '123', ...adjustment, newTotalDebt: 0 }
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await debtApi.adjust('1', adjustment)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/customers/1/adjust-debt'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(adjustment),
        })
      )
      expect(result).toEqual(mockResponse)
    })
  })
})

