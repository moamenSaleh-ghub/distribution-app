import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './Pages.css'

function LoginPage() {
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001'
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      })

      // Check if response is ok first
      if (!response.ok) {
        // Handle non-200 responses
        let errorData = {}
        try {
          const text = await response.text()
          errorData = text ? JSON.parse(text) : {}
        } catch (parseError) {
          console.error('Failed to parse error response:', parseError)
        }
        setError(errorData.message || `Server error: ${response.status} ${response.statusText}`)
        setLoading(false)
        return
      }

      // Parse successful response
      let data
      try {
        const text = await response.text()
        if (!text) {
          setError('Empty response from server')
          setLoading(false)
          return
        }
        data = JSON.parse(text)
      } catch (parseError) {
        console.error('Failed to parse response:', parseError)
        setError(`Server error: Invalid response format`)
        setLoading(false)
        return
      }

      if (data.token) {
        // Save token to localStorage
        localStorage.setItem('authToken', data.token)
        // Redirect to products page
        navigate('/products')
      } else {
        setError(data.message || 'No token received')
      }
    } catch (err) {
      console.error('Login error:', err)
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError('Network error: Could not connect to server. Please check your connection.')
      } else {
        setError(`Error: ${err.message || 'Failed to connect to server. Please try again.'}`)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="form-container" style={{ maxWidth: '400px', margin: '100px auto' }}>
      <h3>Login</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="login-password">Password *</label>
          <input
            id="login-password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoFocus
            disabled={loading}
          />
        </div>

        {error && (
          <div style={{ color: 'red', marginBottom: '1rem', fontSize: '0.9rem' }}>
            {error}
          </div>
        )}

        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default LoginPage

