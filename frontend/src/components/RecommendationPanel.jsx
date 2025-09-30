import React, { useEffect, useState } from 'react'
import api from '../api'

export default function RecommendationPanel({ token }) {
  const [recommendations, setRecommendations] = useState([])
  const [status, setStatus] = useState(token ? 'loading' : 'idle')

  useEffect(() => {
    async function fetchRecommendations() {
      if (!token) {
        setStatus('idle')
        setRecommendations([])
        return
      }
      setStatus('loading')
      try {
        const { data } = await api.get('/recommendations')
        setRecommendations(data.recommendations)
        setStatus('loaded')
      } catch (error) {
        console.error(error)
        setStatus('error')
      }
    }
    fetchRecommendations()

    if (!token) return undefined
    const handler = () => fetchRecommendations()
    window.addEventListener('rating:created', handler)
    return () => window.removeEventListener('rating:created', handler)
  }, [token])

  return (
    <section className="card">
      <h2>Recommended for you</h2>
      {status === 'loading' && <p>Gathering personalized suggestions...</p>}
      {status === 'error' && <p>We need more ratings to craft recommendations. Start rating!</p>}
      {status === 'idle' && <p>Create an account or log in to see personalized ideas.</p>}
      {status === 'loaded' && (
        <div className="grid">
          {recommendations.map((rec) => (
            <div key={rec.item.id} className="recommendation-item">
              <h3>{rec.item.title}</h3>
              <p>{rec.item.description}</p>
              <small>
                Based on {rec.strategy} signals · Estimated score {rec.score.toFixed(2)}
              </small>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
