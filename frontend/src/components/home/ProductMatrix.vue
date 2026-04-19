<template>
  <section id="products" class="section bg-canvas">
    <div class="max-w-7xl mx-auto">
      <div class="mb-16 reveal">
        <p class="label-tag mb-4">Products</p>
        <h2 class="text-3xl md:text-4xl font-bold text-ink-primary mb-3">产品矩阵</h2>
        <p class="text-ink-secondary max-w-md">三款旗舰产品，覆盖视觉、交互、陪伴三大场景</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <router-link
          v-for="(product, i) in productCards"
          :key="product.slug"
          :to="`/products/${product.slug}`"
          class="card group p-7 flex flex-col gap-6 reveal"
          :class="`reveal-delay-${i + 1}`"
        >
          <!-- Visual area -->
          <div class="w-full aspect-video rounded bg-surface border border-line-base flex items-center justify-center overflow-hidden relative">
            <div class="absolute inset-0 bg-grid-subtle opacity-60" />
            <span class="relative text-5xl group-hover:scale-110 transition-transform duration-300">{{ product.emoji }}</span>
          </div>

          <div class="flex-1">
            <div class="flex items-center gap-2 mb-3">
              <span class="label-tag">{{ product.category }}</span>
              <span class="text-2xs text-ink-muted font-mono">{{ product.id }}</span>
            </div>
            <h3 class="text-lg font-semibold text-ink-primary mb-2 group-hover:text-blue-bright transition-colors">
              {{ product.name }}
            </h3>
            <p class="text-ink-secondary text-sm leading-relaxed">{{ product.tagline }}</p>
          </div>

          <div class="flex items-center gap-1 text-blue-base text-sm font-medium border-t border-line-faint pt-4">
            查看详情
            <svg class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const productCards = [
  {
    slug: 'ai-glasses',
    id: 'VISION G1',
    category: 'AI眼镜',
    name: 'AI眼镜 VISION G1',
    tagline: '实时AI视觉识别，让每一次凝视都成为智能交互的起点。',
    emoji: '🥽',
  },
  {
    slug: 'ai-robot',
    id: 'NEXUS R2',
    category: 'AI机器人',
    name: 'AI机器人 NEXUS R2',
    tagline: '自主感知移动，自然语言交互，企业与家庭场景双覆盖。',
    emoji: '🤖',
  },
  {
    slug: 'ai-toy',
    id: 'MOCHI A1',
    category: 'AI玩具',
    name: 'AI玩具 MOCHI A1',
    tagline: '情感化交互，自适应学习，陪伴孩子探索无限可能。',
    emoji: '🧸',
  },
]
</script>
