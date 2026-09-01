import { createContext, useContext } from 'react'

import type { Cart } from './api'

export type CartContextValue = {
  cart: Cart | null
  error: string | null
  addToCart: (productId: number, quantity?: number) => Promise<void>
  setQuantity: (productId: number, quantity: number) => Promise<void>
  removeFromCart: (productId: number) => Promise<void>
  refresh: () => Promise<void>
}

export const CartContext = createContext<CartContextValue | null>(null)

export function useCart(): CartContextValue {
  const context = useContext(CartContext)
  if (!context) throw new Error('useCart must be used within a CartProvider')
  return context
}
