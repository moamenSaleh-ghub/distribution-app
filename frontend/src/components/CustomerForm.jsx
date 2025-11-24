import React, { useState } from 'react'
import '../pages/Pages.css'

function CustomerForm({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    phone: '',
    email: '',
    notes: '',
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const data = {
      ...formData,
      email: formData.email || null,
      notes: formData.notes || null,
    }
    onSubmit(data)
  }

  return (
    <div className="form-container">
      <h3>Add Customer</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="customer-name">Name *</label>
          <input
            id="customer-name"
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="customer-location">Location *</label>
          <input
            id="customer-location"
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="customer-phone">Phone *</label>
          <input
            id="customer-phone"
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="customer-email">Email</label>
          <input
            id="customer-email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="customer-notes">Notes</label>
          <textarea
            id="customer-notes"
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
            Create
          </button>
        </div>
      </form>
    </div>
  )
}

export default CustomerForm

