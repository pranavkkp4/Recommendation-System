import React, { useEffect } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './hooks/useAuth'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import Dashboard from './components/Dashboard'
import api from './api'

function AuthenticatedApp() {
  const { token, setUser } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchProfile() {
      if (!token) {
        navigate('/login')
        return
      }
      try {
        const { data } = await api.get('/users/me')
        setUser(data)
      } catch (error) {
        console.error('Failed to fetch profile', error)
        localStorage.removeItem('token')
        navigate('/login')
      }
    }
    fetchProfile()
  }, [token, navigate, setUser])

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

function PublicRoutes() {
  const { token } = useAuth()
  if (token) {
    return <Navigate to="/" replace />
  }

  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route path="/register" element={<RegisterForm />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

function Router() {
  const { token } = useAuth()
  return token ? <AuthenticatedApp /> : <PublicRoutes />
}

export default function App() {
  return (
    <AuthProvider>
      <Router />
    </AuthProvider>
  )
}
