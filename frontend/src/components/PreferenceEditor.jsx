import React, { useState } from 'react'
import api from '../api'

const SUGGESTED_TAGS = [
  'science fiction',
  'thriller',
  'drama',
  'productivity',
  'self-help',
  'electronics',
  'fitness',
  'software',
  'career'
]

export default function PreferenceEditor() {
  const [input, setInput] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = async (event) => {
    event.preventDefault()
    const tags = input
      .split(',')
      .map((tag) => tag.trim())
      .filter(Boolean)
    if (!tags.length) {
      setMessage('Add at least one tag to update your profile preferences.')
      return
    }
    try {
      await api.post('/users/me/preferences', { tags })
      setMessage('Preferences updated. We will blend them into future recommendations!')
    } catch (error) {
      setMessage('Could not update preferences right now.')
    }
  }

  return (
    <section className="card">
      <h2>Tune your interests</h2>
      <p>List a few topics separated by commas to guide the content-based recommender.</p>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={3}
          placeholder="e.g. science fiction, productivity, electronics"
          value={input}
          onChange={(event) => setInput(event.target.value)}
        />
        <button className="primary" type="submit">
          Save interests
        </button>
      </form>
      {message && <p>{message}</p>}
      <div>
        <strong>Suggested tags:</strong>{' '}
        {SUGGESTED_TAGS.map((tag) => (
          <span
            key={tag}
            className="tag"
            style={{ cursor: 'pointer' }}
            onClick={() => setInput((prev) => (prev ? `${prev}, ${tag}` : tag))}
          >
            {tag}
          </span>
        ))}
      </div>
    </section>
  )
}
