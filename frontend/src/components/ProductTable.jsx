import React from 'react'
import '../pages/Pages.css'

function ProductTable({ products, onEdit, loading }) {
  if (loading) {
    return <div>Loading products...</div>
  }

  if (products.length === 0) {
    return <div>No products found</div>
  }

  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Base Buying Price</th>
          <th>Base Selling Price</th>
          <th>Discount %</th>
          <th>Effective Selling Price</th>
          <th>Active</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr key={product.id}>
            <td>{product.name}</td>
            <td>${product.baseBuyingPrice?.toFixed(2)}</td>
            <td>${product.baseSellingPrice?.toFixed(2)}</td>
            <td>{product.discountPercent || 0}%</td>
            <td>${product.effectiveSellingPrice?.toFixed(2) || product.baseSellingPrice?.toFixed(2)}</td>
            <td>{product.isActive ? 'Yes' : 'No'}</td>
            <td>
              <button
                onClick={() => onEdit(product)}
                className="btn btn-primary"
                style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
              >
                Edit
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default ProductTable

