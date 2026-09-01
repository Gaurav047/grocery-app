import { useEffect, useState } from 'react'

import { api } from '../api'
import type { Category, Product } from '../api'
import { useCart } from '../cart-context'

export default function CatalogPage() {
  const { addToCart, error: cartError } = useCart()
  const [categories, setCategories] = useState<Category[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.listCategories().then(setCategories).catch(() => setCategories([]))
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(true)
      api
        .listProducts({ search, category: activeCategory })
        .then((items) => {
          setProducts(items)
          setError(null)
        })
        .catch((err: Error) => setError(err.message))
        .finally(() => setLoading(false))
    }, 250)
    return () => clearTimeout(timer)
  }, [search, activeCategory])

  return (
    <section>
      <div className="toolbar">
        <input
          className="search"
          type="search"
          placeholder="Search groceries…"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          aria-label="Search groceries"
        />
        <div className="chips">
          <button
            className={activeCategory === '' ? 'chip active' : 'chip'}
            onClick={() => setActiveCategory('')}
          >
            All
          </button>
          {categories.map((category) => (
            <button
              key={category.id}
              className={activeCategory === category.slug ? 'chip active' : 'chip'}
              onClick={() => setActiveCategory(category.slug)}
            >
              {category.name}
            </button>
          ))}
        </div>
      </div>

      {(error ?? cartError) && <p className="error">{error ?? cartError}</p>}
      {loading && <p className="muted">Loading products…</p>}
      {!loading && products.length === 0 && <p className="muted">No products match your search.</p>}

      <div className="grid">
        {products.map((product) => (
          <article key={product.id} className="card">
            <img src={product.image_url} alt={product.name} loading="lazy" />
            <h3>{product.name}</h3>
            <p className="muted">{product.description}</p>
            <p className="price">
              ${product.price.toFixed(2)} <span className="muted">/ {product.unit}</span>
            </p>
            <button
              className="primary"
              disabled={product.stock === 0}
              onClick={() => void addToCart(product.id)}
            >
              {product.stock === 0 ? 'Out of stock' : 'Add to cart'}
            </button>
          </article>
        ))}
      </div>
    </section>
  )
}
