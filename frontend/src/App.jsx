import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import ProductsPage from './pages/ProductsPage'
import CustomersPage from './pages/CustomersPage'
import CustomerDetailPage from './pages/CustomerDetailPage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">Distribution App</h1>
            <div className="nav-links">
              <Link to="/products">Products</Link>
              <Link to="/customers">Customers</Link>
            </div>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<ProductsPage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/customers" element={<CustomersPage />} />
            <Route path="/customers/:id" element={<CustomerDetailPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

