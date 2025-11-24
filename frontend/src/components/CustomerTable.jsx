import React from 'react'
import '../pages/Pages.css'

function CustomerTable({ customers, onRowClick, loading }) {
  if (loading) {
    return <div>Loading customers...</div>
  }

  if (customers.length === 0) {
    return <div>No customers found</div>
  }

  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Location</th>
          <th>Phone</th>
          <th>Total Debt</th>
        </tr>
      </thead>
      <tbody>
        {customers.map((customer) => (
          <tr key={customer.id} onClick={() => onRowClick(customer.id)}>
            <td>{customer.name}</td>
            <td>{customer.location}</td>
            <td>{customer.phone}</td>
            <td>${customer.totalDebt?.toFixed(2) || '0.00'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default CustomerTable

