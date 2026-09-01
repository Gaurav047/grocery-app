export type Category = {
  id: number
  name: string
  slug: string
}

export type Product = {
  id: number
  name: string
  description: string
  price: number
  unit: string
  image_url: string
  stock: number
  category: Category
}

export type CartItem = {
  product: Product
  quantity: number
  line_total: number
}

export type Cart = {
  cart_id: string
  items: CartItem[]
  subtotal: number
  item_count: number
}

export type Order = {
  id: number
  customer_name: string
  address: string
  total: number
  created_at: string
  items: { product_id: number; product_name: string; unit_price: number; quantity: number }[]
}

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const CART_ID_KEY = 'grocery.cartId'

export function getCartId(): string {
  let cartId = localStorage.getItem(CART_ID_KEY)
  if (!cartId) {
    cartId = crypto.randomUUID()
    localStorage.setItem(CART_ID_KEY, cartId)
  }
  return cartId
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}/api${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      'X-Cart-Id': getCartId(),
      ...init.headers,
    },
  })
  if (!response.ok) {
    const detail = await response.json().catch(() => null)
    throw new Error(detail?.detail ?? `Request failed with ${response.status}`)
  }
  return response.json() as Promise<T>
}

export const api = {
  listCategories: () => request<Category[]>('/categories'),
  listProducts: (params: { search?: string; category?: string }) => {
    const query = new URLSearchParams()
    if (params.search) query.set('search', params.search)
    if (params.category) query.set('category', params.category)
    const suffix = query.toString() ? `?${query}` : ''
    return request<Product[]>(`/products${suffix}`)
  },
  getCart: () => request<Cart>('/cart'),
  addToCart: (productId: number, quantity = 1) =>
    request<Cart>('/cart/items', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId, quantity }),
    }),
  setQuantity: (productId: number, quantity: number) =>
    request<Cart>(`/cart/items/${productId}`, {
      method: 'PATCH',
      body: JSON.stringify({ quantity }),
    }),
  removeFromCart: (productId: number) =>
    request<Cart>(`/cart/items/${productId}`, { method: 'DELETE' }),
  checkout: (customerName: string, address: string) =>
    request<Order>('/orders', {
      method: 'POST',
      body: JSON.stringify({ customer_name: customerName, address }),
    }),
  listOrders: () => request<Order[]>('/orders'),
}
