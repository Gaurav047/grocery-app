import { Link } from 'react-router-dom'

import { useCart } from '../cart-context'

export default function CartPage() {
  const { cart, error, setQuantity, removeFromCart } = useCart()

  if (!cart) return <p className="muted">Loading cart…</p>

  if (cart.items.length === 0) {
    return (
      <section className="empty">
        <h2>Your cart is empty</h2>
        <Link className="primary button" to="/">
          Start shopping
        </Link>
      </section>
    )
  }

  return (
    <section>
      <h2>Your cart</h2>
      {error && <p className="error">{error}</p>}
      <ul className="cart-list">
        {cart.items.map((item) => (
          <li key={item.product.id} className="cart-row">
            <img src={item.product.image_url} alt={item.product.name} />
            <div className="cart-row-info">
              <strong>{item.product.name}</strong>
              <span className="muted">
                ${item.product.price.toFixed(2)} / {item.product.unit}
              </span>
            </div>
            <div className="qty">
              <button
                aria-label={`Decrease ${item.product.name}`}
                onClick={() => void setQuantity(item.product.id, item.quantity - 1)}
              >
                −
              </button>
              <span>{item.quantity}</span>
              <button
                aria-label={`Increase ${item.product.name}`}
                onClick={() => void setQuantity(item.product.id, item.quantity + 1)}
              >
                +
              </button>
            </div>
            <span className="line-total">${item.line_total.toFixed(2)}</span>
            <button className="link" onClick={() => void removeFromCart(item.product.id)}>
              Remove
            </button>
          </li>
        ))}
      </ul>
      <div className="summary">
        <span>Subtotal</span>
        <strong>${cart.subtotal.toFixed(2)}</strong>
      </div>
      <Link className="primary button" to="/checkout">
        Checkout
      </Link>
    </section>
  )
}
