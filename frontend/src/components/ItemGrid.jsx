import React from 'react'
import RateItemCard from './RateItemCard'

export default function ItemGrid({ items }) {
  if (!items.length) {
    return null
  }
  return (
    <section className="card">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>Catalog</h2>
          <p>Rate at least three items to unlock smarter recommendations.</p>
        </div>
      </header>
      <div className="grid">
        {items.map((item) => (
          <RateItemCard key={item.id} item={item} />
        ))}
      </div>
    </section>
  )
}
