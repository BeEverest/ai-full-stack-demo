<template>
  <section class="relative pt-32 pb-20 px-4 md:px-8 bg-canvas overflow-hidden">
    <div class="absolute inset-0 bg-grid-subtle opacity-100 pointer-events-none" />
    <div class="absolute top-1/2 right-0 -translate-y-1/2 w-[400px] h-[400px] rounded-full bg-blue-base/5 blur-3xl pointer-events-none" />

    <div class="relative max-w-6xl mx-auto flex flex-col md:flex-row items-center gap-12">
      <!-- Text area -->
      <div class="flex-1 text-center md:text-left">
        <span class="label-tag mb-6 inline-flex">{{ categoryLabel }}</span>
        <h1 class="text-4xl md:text-6xl font-bold text-ink-primary mb-4 leading-tight">{{ product.name }}</h1>
        <p class="text-xl text-blue-gradient font-medium mb-6">{{ product.tagline }}</p>
        <p class="text-ink-secondary leading-relaxed mb-8 max-w-lg">{{ product.description }}</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
          <AppBtn variant="primary" size="lg" to="/contact">预约体验</AppBtn>
          <AppBtn variant="outline" size="lg" to="/contact">商务咨询</AppBtn>
        </div>
      </div>

      <!-- Product visual -->
      <div class="flex-1 flex items-center justify-center">
        <div
          class="w-full max-w-sm aspect-square rounded-2xl bg-surface border border-line-base flex items-center justify-center text-8xl animate-float relative overflow-hidden"
        >
          <div class="absolute inset-0 bg-grid-subtle opacity-60" />
          <span class="relative">{{ emoji }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppBtn from '@/components/common/AppBtn.vue'
import type { ProductDetail } from '@/types'

const props = defineProps<{ product: ProductDetail }>()

const categoryMap: Record<string, string> = {
  glasses: 'AI眼镜',
  robot: 'AI机器人',
  toy: 'AI玩具',
}
const emojiMap: Record<string, string> = {
  glasses: '🥽',
  robot: '🤖',
  toy: '🧸',
}
const categoryLabel = computed(() => categoryMap[props.product.category] ?? props.product.category)
const emoji = computed(() => emojiMap[props.product.category] ?? '📦')
</script>
