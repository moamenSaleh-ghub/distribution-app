import React, { useState } from 'react'
import '../pages/Pages.css'

function DebtAdjustmentForm({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    amount: '',
    reason: '',
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
      amount: parseFloat(formData.amount),
      reason: formData.reason,
    }
    onSubmit(data)
  }

  return (
    <div className="form-container">
      <h3>Adjust Debt</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Amount *</label>
          <input
            type="number"
            step="0.01"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            required
            placeholder="Negative to decrease debt, positive to increase"
          />
          <small style={{ color: '#666', display: 'block', marginTop: '0.25rem' }}>
            Use negative values (e.g., -200) to decrease debt, positive to increase
          </small>
        </div>

        <div className="form-group">
          <label>Reason *</label>
          <textarea
            name="reason"
            value={formData.reason}
            onChange={handleChange}
            required
            placeholder="e.g., Customer paid 200 in cash"
          />
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn btn-primary">
            Adjust Debt
          </button>
        </div>
      </form>
    </div>
  )
}

export default DebtAdjustmentForm

