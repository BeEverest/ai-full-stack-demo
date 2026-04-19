<template>
  <section class="section bg-surface">
    <div class="max-w-6xl mx-auto">
      <div class="mb-12 reveal">
        <p class="label-tag mb-4">Features</p>
        <h2 class="text-3xl font-bold text-ink-primary">核心功能</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="(f, i) in features"
          :key="f.title"
          class="card p-6 reveal"
          :class="`reveal-delay-${Math.min(i + 1, 4)}`"
        >
          <div class="w-10 h-10 rounded bg-blue-dim/60 flex items-center justify-center mb-4 text-xl">
            {{ f.icon }}
          </div>
          <h3 class="text-ink-primary font-semibold mb-2">{{ f.title }}</h3>
          <p class="text-ink-secondary text-sm leading-relaxed">{{ f.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Feature } from '@/types'
defineProps<{ features: Feature[] }>()
</script>
