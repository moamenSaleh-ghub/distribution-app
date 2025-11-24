import React, { useState, useEffect } from 'react'
import { productsApi } from '../api/client'
import '../pages/Pages.css'

function OrderForm({ customerId, onSubmit, onCancel }) {
  const [products, setProducts] = useState([])
  const [items, setItems] = useState([{ productId: '', quantity: '', unitPrice: null }])
  const [formData, setFormData] = useState({
    orderDate: new Date().toISOString().slice(0, 16),
    discount: '',
    paidNow: '',
    notes: '',
  })

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      const response = await productsApi.list({ includeInactive: false })
      setProducts(response.items || [])
    } catch (err) {
      console.error('Failed to load products:', err)
    }
  }

  const handleItemChange = (index, field, value) => {
    const newItems = [...items]
    newItems[index] = { ...newItems[index], [field]: value }
    
    // If product selected and unitPrice not set, fetch product price
    if (field === 'productId' && value) {
      const product = products.find(p => p.id === value)
      if (product && !newItems[index].unitPrice) {
        newItems[index].unitPrice = product.effectiveSellingPrice || product.baseSellingPrice
      }
    }
    
    setItems(newItems)
  }

  const addItem = () => {
    setItems([...items, { productId: '', quantity: '', unitPrice: null }])
  }

  const removeItem = (index) => {
    setItems(items.filter((_, i) => i !== index))
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const orderItems = items
      .filter(item => item.productId && item.quantity)
      .map(item => ({
        productId: item.productId,
        quantity: parseFloat(item.quantity),
        unitPrice: item.unitPrice ? parseFloat(item.unitPrice) : null,
      }))

    if (orderItems.length === 0) {
      alert('Please add at least one item')
      return
    }

    const data = {
      customerId,
      orderDate: formData.orderDate ? new Date(formData.orderDate).toISOString() : null,
      items: orderItems,
      discount: parseFloat(formData.discount) || 0,
      paidNow: parseFloat(formData.paidNow) || 0,
      notes: formData.notes || null,
    }

    onSubmit(data)
  }

  return (
    <div className="form-container">
      <h3>Create Order</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Order Date</label>
          <input
            type="datetime-local"
            name="orderDate"
            value={formData.orderDate}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Items *</label>
          {items.map((item, index) => (
            <div key={index} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem', alignItems: 'center' }}>
              <select
                value={item.productId}
                onChange={(e) => handleItemChange(index, 'productId', e.target.value)}
                required
                style={{ flex: 2 }}
              >
                <option value="">Select Product</option>
                {products.map(p => (
                  <option key={p.id} value={p.id}>
                    {p.name} (${(p.effectiveSellingPrice || p.baseSellingPrice)?.toFixed(2)})
                  </option>
                ))}
              </select>
              <input
                type="number"
                step="1"
                min="1"
                placeholder="Quantity"
                value={item.quantity}
                onChange={(e) => handleItemChange(index, 'quantity', e.target.value)}
                required
                style={{ flex: 1 }}
              />
              <input
                type="number"
                step="0.01"
                min="0"
                placeholder="Unit Price (optional)"
                value={item.unitPrice || ''}
                onChange={(e) => handleItemChange(index, 'unitPrice', e.target.value)}
                style={{ flex: 1 }}
              />
              {items.length > 1 && (
                <button type="button" onClick={() => removeItem(index)} className="btn btn-danger" style={{ padding: '0.5rem' }}>
                  Remove
                </button>
              )}
            </div>
          ))}
          <button type="button" onClick={addItem} className="btn btn-secondary" style={{ marginTop: '0.5rem' }}>
            Add Item
          </button>
        </div>

        <div className="form-group">
          <label>Discount</label>
          <input
            type="number"
            step="0.01"
            min="0"
            name="discount"
            value={formData.discount}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Paid Now</label>
          <input
            type="number"
            step="0.01"
            min="0"
            name="paidNow"
            value={formData.paidNow}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Notes</label>
          <textarea
            name="notes"
            value={formData.notes}
            onChange={handleChange}
          />
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn btn-primary">
            Create Order
          </button>
        </div>
      </form>
    </div>
  )
}

export default OrderForm

