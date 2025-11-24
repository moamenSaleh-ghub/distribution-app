import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { customersApi, ordersApi, debtApi } from '../api/client'
import OrderForm from '../components/OrderForm'
import DebtAdjustmentForm from '../components/DebtAdjustmentForm'
import './Pages.css'

function CustomerDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [customer, setCustomer] = useState(null)
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showOrderForm, setShowOrderForm] = useState(false)
  const [showDebtForm, setShowDebtForm] = useState(false)

  useEffect(() => {
    loadCustomerDetail()
  }, [id])

  const loadCustomerDetail = async () => {
    try {
      setLoading(true)
      setError(null)
      const [customerData, ordersData] = await Promise.all([
        customersApi.get(id),
        ordersApi.getCustomerOrders(id)
      ])
      setCustomer(customerData.customer)
      setOrders(ordersData.items || [])
    } catch (err) {
      setError(err.message || 'Failed to load customer details')
    } finally {
      setLoading(false)
    }
  }

  const handleOrderCreate = async (orderData) => {
    try {
      await ordersApi.create(orderData)
      await loadCustomerDetail()
      setShowOrderForm(false)
    } catch (err) {
      setError(err.message || 'Failed to create order')
    }
  }

  const handleDebtAdjust = async (adjustmentData) => {
    try {
      await debtApi.adjust(id, adjustmentData)
      await loadCustomerDetail()
      setShowDebtForm(false)
    } catch (err) {
      setError(err.message || 'Failed to adjust debt')
    }
  }

  if (loading) {
    return <div className="page-container">Loading...</div>
  }

  if (error && !customer) {
    return (
      <div className="page-container">
        <div className="error-message">{error}</div>
        <button onClick={() => navigate('/customers')} className="btn btn-secondary">
          Back to Customers
        </button>
      </div>
    )
  }

  if (!customer) {
    return <div className="page-container">Customer not found</div>
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <button onClick={() => navigate('/customers')} className="btn btn-secondary">
          ← Back
        </button>
        <h2>{customer.name}</h2>
        <div>
          <button onClick={() => setShowOrderForm(true)} className="btn btn-primary">
            New Order
          </button>
          <button onClick={() => setShowDebtForm(true)} className="btn btn-primary" style={{ marginLeft: '0.5rem' }}>
            Adjust Debt
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="customer-detail">
        <div className="detail-section">
          <h3>Customer Information</h3>
          <div className="detail-grid">
            <div><strong>Location:</strong> {customer.location}</div>
            <div><strong>Phone:</strong> {customer.phone}</div>
            {customer.email && <div><strong>Email:</strong> {customer.email}</div>}
            <div><strong>Total Debt:</strong> ${customer.totalDebt?.toFixed(2) || '0.00'}</div>
            {customer.notes && <div><strong>Notes:</strong> {customer.notes}</div>}
          </div>
        </div>

        {showOrderForm && (
          <OrderForm
            customerId={id}
            onSubmit={handleOrderCreate}
            onCancel={() => setShowOrderForm(false)}
          />
        )}

        {showDebtForm && (
          <DebtAdjustmentForm
            onSubmit={handleDebtAdjust}
            onCancel={() => setShowDebtForm(false)}
          />
        )}

        <div className="detail-section">
          <h3>Recent Orders</h3>
          {orders.length === 0 ? (
            <p>No orders yet</p>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Total Amount</th>
                  <th>Paid Now</th>
                  <th>Debt Change</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td>{new Date(order.orderDate).toLocaleDateString()}</td>
                    <td>${order.totalAmount?.toFixed(2)}</td>
                    <td>${order.paidNow?.toFixed(2)}</td>
                    <td>${order.debtChange?.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}

export default CustomerDetailPage

