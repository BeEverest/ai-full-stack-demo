import client from './client'
import type { Product, ProductDetail, Stat } from '@/types'

export const fetchProducts = (): Promise<Product[]> =>
  client.get('/products')

export const fetchProductDetail = (slug: string): Promise<ProductDetail> =>
  client.get(`/products/${slug}`)

export const fetchStats = (): Promise<Stat[]> =>
  client.get('/stats')
