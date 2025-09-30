import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api'
import { useAuth } from '../hooks/useAuth'

export default function LoginForm() {
  const { setToken } = useAuth()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    try {
      const formData = new URLSearchParams()
      formData.append('username', form.email)
      formData.append('password', form.password)
      const { data } = await api.post('/auth/login', formData)
      localStorage.setItem('token', data.access_token)
      setToken(data.access_token)
      navigate('/')
    } catch (err) {
      setError('Invalid email or password')
    }
  }

  return (
    <div className="container" style={{ maxWidth: 480 }}>
      <div className="card">
        <h2>Log in</h2>
        <p>Rate books, movies, and products to personalize your recommendations.</p>
        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Email</label>
          <input id="email" type="email" name="email" value={form.email} onChange={handleChange} required />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
          />

          {error && <p style={{ color: '#dc2626' }}>{error}</p>}

          <button className="primary" type="submit">
            Sign in
          </button>
        </form>
        <p>
          Need an account? <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  )
}
