<template>
  <div>
    <!-- 加载态 -->
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <div class="flex flex-col items-center gap-4">
        <div class="w-8 h-8 border-2 border-blue-base/30 border-t-blue-base rounded-full animate-spin" />
        <p class="text-ink-secondary text-sm">加载中...</p>
      </div>
    </div>

    <!-- 错误态 -->
    <div v-else-if="error" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <p class="text-ink-secondary mb-4">{{ error }}</p>
        <AppBtn variant="outline" to="/">返回首页</AppBtn>
      </div>
    </div>

    <!-- 内容 -->
    <template v-else-if="product">
      <ProductHero :product="product" />
      <ProductFeatures v-if="product.features.length" :features="product.features" />
      <ProductSpecs v-if="product.specs.length" :specs="product.specs" />

      <!-- 底部 CTA -->
      <section class="section bg-surface text-center">
        <h2 class="text-2xl font-bold text-ink-primary mb-4 reveal">
          对 {{ product.name }} 感兴趣？
        </h2>
        <p class="text-ink-secondary mb-8 reveal reveal-delay-1">立即联系我们，获取专属方案</p>
        <div class="flex flex-col sm:flex-row justify-center gap-4 reveal reveal-delay-2">
          <AppBtn variant="primary" size="lg" to="/contact">预约体验</AppBtn>
          <AppBtn variant="outline" size="lg" to="/">浏览其他产品</AppBtn>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useProductStore } from '@/stores/product'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import ProductHero from '@/components/product/ProductHero.vue'
import ProductFeatures from '@/components/product/ProductFeatures.vue'
import ProductSpecs from '@/components/product/ProductSpecs.vue'
import AppBtn from '@/components/common/AppBtn.vue'

const route = useRoute()
const store = useProductStore()
const { currentProduct: product, loading, error } = storeToRefs(store)

useScrollAnimation()

function load() {
  const slug = route.params.slug as string
  store.loadProductDetail(slug)
  document.title = `产品详情 — AI智能终端`
}

onMounted(load)
watch(() => route.params.slug, load)
</script>
