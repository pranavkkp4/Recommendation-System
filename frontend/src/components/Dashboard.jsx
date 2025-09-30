import React, { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import { useAuth } from '../hooks/useAuth'
import ItemGrid from './ItemGrid'
import RecommendationPanel from './RecommendationPanel'
import RatingHistory from './RatingHistory'
import PreferenceEditor from './PreferenceEditor'

export default function Dashboard() {
  const { setToken, setUser, token, user } = useAuth()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const headerGreeting = useMemo(() => {
    if (!user?.full_name) return 'Welcome back!'
    const [firstName] = user.full_name.split(' ')
    return `Hello, ${firstName}!`
  }, [user])

  useEffect(() => {
    async function loadData() {
      try {
        const { data } = await api.get('/items')
        setItems(data)
      } catch (err) {
        console.error(err)
        setError('Unable to load catalog items.')
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    navigate('/login')
  }

  if (loading) {
    return <div className="container">Loading your personalized dashboard...</div>
  }

  if (error) {
    return <div className="container">{error}</div>
  }

  return (
    <div>
      <nav className="navbar">
        <h1>Personalized Recommender</h1>
        <div className="badge">
          <span>{headerGreeting}</span>
          <button className="secondary" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </nav>
      <main className="container">
        <RecommendationPanel token={token} />
        <PreferenceEditor />
        <ItemGrid items={items} />
        <RatingHistory />
      </main>
    </div>
  )
}
