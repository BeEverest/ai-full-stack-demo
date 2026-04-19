<template>
  <section class="section bg-surface">
    <div class="max-w-7xl mx-auto">
      <div class="mb-16 reveal">
        <p class="label-tag mb-4">Technology</p>
        <h2 class="text-3xl md:text-4xl font-bold text-ink-primary mb-3">核心技术</h2>
        <p class="text-ink-secondary">自研技术栈，构建AI硬件全栈能力</p>
      </div>

      <!-- Stats -->
      <div v-if="stats.length > 0" class="grid grid-cols-2 md:grid-cols-4 gap-px bg-line-base rounded-lg overflow-hidden mb-16 reveal reveal-delay-1">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="bg-surface px-6 py-8 text-center"
        >
          <div class="text-3xl md:text-4xl font-bold font-mono text-blue-gradient mb-2">
            {{ stat.value }}<span class="text-xl text-ink-secondary ml-0.5">{{ stat.unit }}</span>
          </div>
          <p class="text-ink-secondary text-sm">{{ stat.label }}</p>
        </div>
      </div>

      <!-- Tech highlight cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <div
          v-for="(item, i) in highlights"
          :key="item.title"
          class="card p-6 reveal"
          :class="`reveal-delay-${i + 1}`"
        >
          <div class="w-10 h-10 rounded bg-blue-dim/60 flex items-center justify-center mb-4 text-xl">
            {{ item.icon }}
          </div>
          <h3 class="text-ink-primary font-semibold mb-2 text-sm">{{ item.title }}</h3>
          <p class="text-ink-secondary text-sm leading-relaxed">{{ item.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useProductStore } from '@/stores/product'
import { storeToRefs } from 'pinia'

const store = useProductStore()
const { stats } = storeToRefs(store)
onMounted(() => store.loadStats())

const highlights = [
  {
    icon: '🧠',
    title: '端侧AI推理',
    desc: '自研轻量化模型，毫秒级本地推理，无需依赖云端网络。',
  },
  {
    icon: '👁️',
    title: '计算机视觉',
    desc: '实时目标检测、场景理解，视觉感知精度行业领先。',
  },
  {
    icon: '🎙️',
    title: '自然语言交互',
    desc: '多轮对话理解，支持方言与专业领域语料微调。',
  },
  {
    icon: '🔋',
    title: '超低功耗设计',
    desc: '硬件协同优化，全天候续航，极致轻量化形态。',
  },
]
</script>
