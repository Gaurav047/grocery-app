import { BrowserRouter, Link, Navigate, NavLink, Route, Routes } from 'react-router-dom'

import { CartProvider } from './CartContext'
import { useCart } from './cart-context'
import CartPage from './pages/CartPage'
import CatalogPage from './pages/CatalogPage'
import CheckoutPage from './pages/CheckoutPage'
import OrdersPage from './pages/OrdersPage'

function Header() {
  const { cart } = useCart()
  const count = cart?.item_count ?? 0

  return (
    <header className="header">
      <Link to="/" className="brand">
        <span aria-hidden="true">🛒</span> FreshCart
      </Link>
      <nav className="nav">
        <NavLink to="/">Shop</NavLink>
        <NavLink to="/orders">Orders</NavLink>
        <NavLink to="/cart" className="cart-link">
          Cart
          {count > 0 && <span className="badge">{count}</span>}
        </NavLink>
      </nav>
    </header>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <CartProvider>
        <Header />
        <main className="main">
          <Routes>
            <Route path="/" element={<CatalogPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </CartProvider>
    </BrowserRouter>
  )
}
