import React, { useEffect, useState } from 'react'
import api from '../api'

export default function RatingHistory() {
  const [ratings, setRatings] = useState([])

  useEffect(() => {
    async function loadRatings() {
      try {
        const { data } = await api.get('/ratings/me')
        setRatings(data)
      } catch (error) {
        setRatings([])
      }
    }
    loadRatings()

    const handler = () => loadRatings()
    window.addEventListener('rating:created', handler)
    return () => window.removeEventListener('rating:created', handler)
  }, [])

  if (!ratings.length) {
    return null
  }

  return (
    <section className="card">
      <h2>Your latest ratings</h2>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        {ratings.map((rating) => (
          <li key={rating.id} style={{ marginBottom: '0.5rem' }}>
            <strong>{rating.item.title}</strong> — {rating.score.toFixed(1)} ★
          </li>
        ))}
      </ul>
    </section>
  )
}
