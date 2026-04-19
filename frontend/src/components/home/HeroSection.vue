<template>
  <section class="relative min-h-screen flex items-center overflow-hidden bg-canvas">
    <!-- Subtle grid -->
    <div class="absolute inset-0 bg-grid-subtle opacity-100 pointer-events-none" />
    <!-- Single restrained glow -->
    <div class="absolute top-1/2 right-1/4 -translate-y-1/2 w-[480px] h-[480px] rounded-full bg-blue-base/6 blur-3xl pointer-events-none" />

    <div class="relative z-10 w-full max-w-7xl mx-auto px-4 md:px-8 lg:px-16 xl:px-24 pt-32 pb-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

        <!-- Left: Editorial copy -->
        <div>
          <div class="label-tag mb-8 reveal">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-bright animate-glow-pulse" />
            下一代 AI 硬件终端
          </div>

          <h1 class="text-5xl md:text-6xl xl:text-7xl font-bold leading-[1.05] tracking-tight text-ink-primary mb-6 reveal reveal-delay-1">
            智能，<br />
            <span class="text-blue-gradient">从此触手可及</span>
          </h1>

          <p class="text-ink-secondary text-lg leading-relaxed mb-10 max-w-md reveal reveal-delay-2">
            融合前沿人工智能技术与精密硬件工程，重新定义人与智能的交互边界。
          </p>

          <div class="flex flex-col sm:flex-row items-start gap-4 reveal reveal-delay-3">
            <AppBtn variant="primary" size="lg" to="/#products">探索产品</AppBtn>
            <AppBtn variant="outline" size="lg" to="/contact">商务合作</AppBtn>
          </div>
        </div>

        <!-- Right: Product lineup indicator -->
        <div class="hidden lg:flex flex-col gap-4 reveal reveal-delay-2">
          <div
            v-for="(p, i) in productLines"
            :key="p.slug"
            class="card flex items-center gap-5 px-6 py-5 group cursor-default"
            :style="{ transitionDelay: `${(i + 2) * 80}ms` }"
          >
            <div class="w-10 h-10 rounded bg-blue-dim/60 flex items-center justify-center text-blue-bright shrink-0 group-hover:bg-blue-dim transition-colors">
              <component :is="p.icon" class="w-5 h-5" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-ink-primary text-sm font-medium">{{ p.name }}</p>
              <p class="text-ink-secondary text-xs mt-0.5 truncate">{{ p.tagline }}</p>
            </div>
            <div class="text-2xs text-ink-muted font-mono tracking-wider">{{ p.id }}</div>
          </div>
        </div>
      </div>

      <!-- Bottom metrics strip -->
      <div class="mt-20 pt-8 border-t border-line-faint grid grid-cols-3 gap-8 reveal reveal-delay-4">
        <div v-for="m in metrics" :key="m.label" class="text-center">
          <p class="text-2xl md:text-3xl font-bold text-ink-primary font-mono">{{ m.value }}</p>
          <p class="text-ink-secondary text-xs mt-1 tracking-wide">{{ m.label }}</p>
        </div>
      </div>
    </div>

    <!-- Scroll hint -->
    <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1.5 text-ink-muted text-2xs animate-float">
      <span class="tracking-widest uppercase">Scroll</span>
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import AppBtn from '@/components/common/AppBtn.vue'
import { useScrollAnimation } from '@/composables/useScrollAnimation'

useScrollAnimation()

const productLines = [
  {
    slug: 'ai-glasses',
    id: 'VISION G1',
    name: 'AI 眼镜',
    tagline: '实时视觉识别，空间 AI 交互',
    icon: {
      render() {
        return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
          h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '1.5', d: 'M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z M15 12a3 3 0 11-6 0 3 3 0 016 0z' }),
        ])
      },
    },
  },
  {
    slug: 'ai-robot',
    id: 'NEXUS R2',
    name: 'AI 机器人',
    tagline: '7B 大模型驱动，SLAM 自主导航',
    icon: {
      render() {
        return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
          h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '1.5', d: 'M9 3.75H6.912a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H15M9 3.75h6m-6 0a1.125 1.125 0 01-1.125-1.125v0a1.125 1.125 0 011.125-1.125h6a1.125 1.125 0 011.125 1.125v0A1.125 1.125 0 0115 3.75m-6 0h6' }),
        ])
      },
    },
  },
  {
    slug: 'ai-toy',
    id: 'MOCHI A1',
    name: 'AI 玩具',
    tagline: '情感引擎，自适应学习陪伴',
    icon: {
      render() {
        return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
          h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '1.5', d: 'M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z' }),
        ])
      },
    },
  },
]

const metrics = [
  { value: '60+', label: '自研技术专利' },
  { value: '80+', label: '硬件工程师' },
  { value: '120+', label: '合作伙伴' },
]

import { h } from 'vue'
</script>
