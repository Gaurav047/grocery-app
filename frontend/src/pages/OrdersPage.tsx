import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { api } from '../api'
import type { Order } from '../api'

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .listOrders()
      .then(setOrders)
      .catch((err: Error) => setError(err.message))
  }, [])

  if (error) return <p className="error">{error}</p>
  if (!orders) return <p className="muted">Loading orders…</p>

  if (orders.length === 0) {
    return (
      <section className="empty">
        <h2>No orders yet</h2>
        <Link className="primary button" to="/">
          Start shopping
        </Link>
      </section>
    )
  }

  return (
    <section>
      <h2>Your orders</h2>
      {orders.map((order) => (
        <article key={order.id} className="order">
          <header>
            <strong>Order #{order.id}</strong>
            <span className="muted">{new Date(order.created_at).toLocaleString()}</span>
          </header>
          <ul>
            {order.items.map((item) => (
              <li key={item.product_id}>
                {item.quantity} × {item.product_name}
                <span className="muted"> — ${(item.unit_price * item.quantity).toFixed(2)}</span>
              </li>
            ))}
          </ul>
          <div className="summary">
            <span>Total</span>
            <strong>${order.total.toFixed(2)}</strong>
          </div>
          <p className="muted">
            Delivering to {order.customer_name}, {order.address}
          </p>
        </article>
      ))}
    </section>
  )
}
