import React, { useState, useEffect } from 'react'
import '../pages/Pages.css'

function ProductForm({ product, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    baseBuyingPrice: '',
    baseSellingPrice: '',
    discountPercent: '',
    imageKey: '',
    isActive: true,
  })

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || '',
        baseBuyingPrice: product.baseBuyingPrice || '',
        baseSellingPrice: product.baseSellingPrice || '',
        discountPercent: product.discountPercent || '',
        imageKey: product.imageKey || '',
        isActive: product.isActive !== undefined ? product.isActive : true,
      })
    }
  }, [product])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const data = {
      ...formData,
      baseBuyingPrice: parseFloat(formData.baseBuyingPrice),
      baseSellingPrice: parseFloat(formData.baseSellingPrice),
      discountPercent: formData.discountPercent ? parseFloat(formData.discountPercent) : 0,
      imageKey: formData.imageKey || null,
    }
    onSubmit(data)
  }

  return (
    <div className="form-container">
      <h3>{product ? 'Edit Product' : 'Add Product'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Base Buying Price *</label>
          <input
            type="number"
            step="0.01"
            min="0"
            name="baseBuyingPrice"
            value={formData.baseBuyingPrice}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Base Selling Price *</label>
          <input
            type="number"
            step="0.01"
            min="0"
            name="baseSellingPrice"
            value={formData.baseSellingPrice}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Discount Percent (0-100)</label>
          <input
            type="number"
            step="0.01"
            min="0"
            max="100"
            name="discountPercent"
            value={formData.discountPercent}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Image Key (S3)</label>
          <input
            type="text"
            name="imageKey"
            value={formData.imageKey}
            onChange={handleChange}
            placeholder="products/image.jpg"
          />
        </div>

        <div className="form-group">
          <label>
            <input
              type="checkbox"
              name="isActive"
              checked={formData.isActive}
              onChange={handleChange}
            />
            Active
          </label>
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn btn-primary">
            {product ? 'Update' : 'Create'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default ProductForm

