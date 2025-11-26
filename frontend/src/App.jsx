import React, { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom'
import ProductsPage from './pages/ProductsPage'
import CustomersPage from './pages/CustomersPage'
import CustomerDetailPage from './pages/CustomerDetailPage'
import LoginPage from './pages/LoginPage'
import './App.css'

// Protected Route component
function ProtectedRoute({ children }) {
  const navigate = useNavigate()
  const location = useLocation()
  const [isAuthenticated, setIsAuthenticated] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('authToken')
    if (!token) {
      navigate('/login', { state: { from: location.pathname } })
    } else {
      setIsAuthenticated(true)
    }
  }, [navigate, location])

  if (isAuthenticated === null) {
    return <div>Loading...</div>
  }

  return isAuthenticated ? children : null
}

function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()
  const token = localStorage.getItem('authToken')

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    navigate('/login')
  }

  // Don't show navbar on login page
  if (location.pathname === '/login') {
    return null
  }

  return (
    <nav className="navbar">
      <div className="nav-container">
        <h1 className="nav-title">Distribution App</h1>
        <div className="nav-links">
          <Link to="/products">Products</Link>
          <Link to="/customers">Customers</Link>
          {token && (
            <button 
              onClick={handleLogout} 
              className="btn btn-secondary"
              style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }}
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <ProductsPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/products" 
              element={
                <ProtectedRoute>
                  <ProductsPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/customers" 
              element={
                <ProtectedRoute>
                  <CustomersPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/customers/:id" 
              element={
                <ProtectedRoute>
                  <CustomerDetailPage />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

