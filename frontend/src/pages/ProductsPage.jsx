import React, { useState, useEffect } from 'react'
import { productsApi } from '../api/client'
import ProductForm from '../components/ProductForm'
import ProductTable from '../components/ProductTable'
import './Pages.css'

function ProductsPage() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      setError(null)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await productsApi.list(params)
      setProducts(response.items || [])
    } catch (err) {
      setError(err.message || 'Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (productData) => {
    try {
      await productsApi.create(productData)
      await loadProducts()
      setShowForm(false)
    } catch (err) {
      setError(err.message || 'Failed to create product')
    }
  }

  const handleUpdate = async (id, productData) => {
    try {
      await productsApi.update(id, productData)
      await loadProducts()
      setEditingProduct(null)
    } catch (err) {
      setError(err.message || 'Failed to update product')
    }
  }

  const handleSearch = (e) => {
    setSearchTerm(e.target.value)
  }

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      loadProducts()
    }, 300)
    return () => clearTimeout(timeoutId)
  }, [searchTerm])

  if (loading && products.length === 0) {
    return <div className="page-container">Loading...</div>
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>Products</h2>
        <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
          {showForm ? 'Cancel' : 'Add Product'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <ProductForm
          onSubmit={handleCreate}
          onCancel={() => setShowForm(false)}
        />
      )}

      {editingProduct && (
        <ProductForm
          product={editingProduct}
          onSubmit={(data) => handleUpdate(editingProduct.id, data)}
          onCancel={() => setEditingProduct(null)}
        />
      )}

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search products..."
          value={searchTerm}
          onChange={handleSearch}
          className="search-input"
        />
      </div>

      <ProductTable
        products={products}
        onEdit={setEditingProduct}
        loading={loading}
      />
    </div>
  )
}

export default ProductsPage

