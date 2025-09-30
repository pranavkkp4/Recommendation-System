import React, { useState } from 'react'
import api from '../api'
import { useAuth } from '../hooks/useAuth'

const STAR_SCALE = [1, 2, 3, 4, 5]

export default function RateItemCard({ item }) {
  const { token, user } = useAuth()
  const [score, setScore] = useState(null)
  const [status, setStatus] = useState('idle')

  const handleRate = async (value) => {
    if (!token) {
      setStatus('login-required')
      return
    }
    setScore(value)
    setStatus('saving')
    try {
      await api.post('/ratings', { item_id: item.id, score: value })
      setStatus('saved')
      window.dispatchEvent(new CustomEvent('rating:created'))
    } catch (error) {
      console.error(error)
      setStatus('error')
    }
  }

  return (
    <div className="card" style={{ boxShadow: 'none', border: '1px solid #e2e8f0' }}>
      <h3>{item.title}</h3>
      <p style={{ minHeight: 60 }}>{item.description}</p>
      <div>
        {(item.tags || '').split(',').filter(Boolean).map((tag) => (
          <span key={tag} className="tag">
            {tag.trim()}
          </span>
        ))}
      </div>
      <div style={{ marginTop: '1rem' }}>
        <div className="rating-stars">
          {STAR_SCALE.map((value) => (
            <button
              key={value}
              type="button"
              className={score && value <= score ? 'active' : ''}
              onClick={() => handleRate(value)}
              aria-label={`Rate ${value} stars`}
            >
              ★
            </button>
          ))}
        </div>
        <small>
          {status === 'saving' && 'Saving rating...'}
          {status === 'saved' && 'Thanks for rating!'}
          {status === 'error' && 'Could not save rating.'}
          {status === 'idle' && user && 'Click a star to rate'}
          {status === 'idle' && !user && 'Sign in to rate'}
          {status === 'login-required' && 'Please log in to rate items.'}
        </small>
      </div>
    </div>
  )
}
