import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { api } from '../api'
import { useCart } from '../cart-context'

export default function CheckoutPage() {
  const { cart, refresh } = useCart()
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [address, setAddress] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  if (cart && cart.items.length === 0) {
    return (
      <section className="empty">
        <h2>Nothing to check out</h2>
        <Link className="primary button" to="/">
          Browse groceries
        </Link>
      </section>
    )
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setSubmitting(true)
    try {
      await api.checkout(name, address)
      await refresh()
      navigate('/orders')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Checkout failed')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="checkout">
      <h2>Checkout</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Full name
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Delivery address
          <input value={address} onChange={(e) => setAddress(e.target.value)} required />
        </label>
        <div className="summary">
          <span>Order total</span>
          <strong>${(cart?.subtotal ?? 0).toFixed(2)}</strong>
        </div>
        <button className="primary" type="submit" disabled={submitting}>
          {submitting ? 'Placing order…' : 'Place order'}
        </button>
      </form>
    </section>
  )
}
