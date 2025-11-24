import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { customersApi } from '../api/client'
import CustomerForm from '../components/CustomerForm'
import CustomerTable from '../components/CustomerTable'
import './Pages.css'

function CustomersPage() {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    loadCustomers()
  }, [])

  const loadCustomers = async () => {
    try {
      setLoading(true)
      setError(null)
      const params = searchTerm ? { search: searchTerm } : {}
      const response = await customersApi.list(params)
      setCustomers(response.items || [])
    } catch (err) {
      setError(err.message || 'Failed to load customers')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (customerData) => {
    try {
      await customersApi.create(customerData)
      await loadCustomers()
      setShowForm(false)
    } catch (err) {
      setError(err.message || 'Failed to create customer')
    }
  }

  const handleSearch = (e) => {
    setSearchTerm(e.target.value)
  }

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      loadCustomers()
    }, 300)
    return () => clearTimeout(timeoutId)
  }, [searchTerm])

  const handleRowClick = (customerId) => {
    navigate(`/customers/${customerId}`)
  }

  if (loading && customers.length === 0) {
    return <div className="page-container">Loading...</div>
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>Customers</h2>
        <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
          {showForm ? 'Cancel' : 'Add Customer'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <CustomerForm
          onSubmit={handleCreate}
          onCancel={() => setShowForm(false)}
        />
      )}

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search customers..."
          value={searchTerm}
          onChange={handleSearch}
          className="search-input"
        />
      </div>

      <CustomerTable
        customers={customers}
        onRowClick={handleRowClick}
        loading={loading}
      />
    </div>
  )
}

export default CustomersPage

