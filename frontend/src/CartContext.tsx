import { useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'

import { api } from './api'
import type { Cart } from './api'
import { CartContext } from './cart-context'
import type { CartContextValue } from './cart-context'

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<Cart | null>(null)
  const [error, setError] = useState<string | null>(null)

  const run = useCallback(async (action: () => Promise<Cart>) => {
    try {
      setCart(await action())
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    }
  }, [])

  const refresh = useCallback(() => run(api.getCart), [run])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const value = useMemo<CartContextValue>(
    () => ({
      cart,
      error,
      refresh,
      addToCart: (productId, quantity = 1) => run(() => api.addToCart(productId, quantity)),
      setQuantity: (productId, quantity) => run(() => api.setQuantity(productId, quantity)),
      removeFromCart: (productId) => run(() => api.removeFromCart(productId)),
    }),
    [cart, error, refresh, run],
  )

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}
