import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchProducts, fetchProductDetail, fetchStats } from '@/api/products'
import type { Product, ProductDetail, Stat } from '@/types'

export const useProductStore = defineStore('product', () => {
  const products = ref<Product[]>([])
  const currentProduct = ref<ProductDetail | null>(null)
  const stats = ref<Stat[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadProducts() {
    if (products.value.length > 0) return
    loading.value = true
    error.value = null
    try {
      products.value = await fetchProducts()
    } catch {
      error.value = '加载产品列表失败'
    } finally {
      loading.value = false
    }
  }

  async function loadProductDetail(slug: string) {
    loading.value = true
    error.value = null
    currentProduct.value = null
    try {
      currentProduct.value = await fetchProductDetail(slug)
    } catch {
      error.value = '加载产品详情失败'
    } finally {
      loading.value = false
    }
  }

  async function loadStats() {
    if (stats.value.length > 0) return
    try {
      stats.value = await fetchStats()
    } catch {
      // 静默失败，stats 为空时页面不展示该 section
    }
  }

  return { products, currentProduct, stats, loading, error, loadProducts, loadProductDetail, loadStats }
})
