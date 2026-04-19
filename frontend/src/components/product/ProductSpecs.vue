<template>
  <section class="section bg-canvas">
    <div class="max-w-3xl mx-auto">
      <div class="mb-12 reveal">
        <p class="label-tag mb-4">Specifications</p>
        <h2 class="text-3xl font-bold text-ink-primary">产品规格</h2>
      </div>
      <div class="card overflow-hidden reveal reveal-delay-1">
        <div
          v-for="spec in specs"
          :key="spec.spec_key"
          class="spec-row px-6"
        >
          <span class="w-40 shrink-0 text-ink-secondary text-sm font-medium">{{ spec.spec_key }}</span>
          <span class="text-ink-primary text-sm">{{ spec.spec_value }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Spec } from '@/types'
defineProps<{ specs: Spec[] }>()
</script>
