<template>
  <footer class="bg-surface border-t border-line-base">
    <div class="max-w-7xl mx-auto px-4 md:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand -->
        <div class="md:col-span-2">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded bg-gradient-blue flex items-center justify-center">
              <span class="text-canvas font-bold text-sm">AI</span>
            </div>
            <span class="font-semibold text-ink-primary">AI智能终端</span>
          </div>
          <p class="text-ink-secondary text-sm leading-relaxed max-w-xs">
            致力于打造下一代AI硬件终端，让智能真正触手可及。
          </p>
        </div>

        <!-- Products -->
        <div>
          <h4 class="text-ink-primary text-xs font-semibold tracking-widest uppercase mb-4">产品</h4>
          <ul class="space-y-2">
            <li v-for="p in products" :key="p.path">
              <router-link
                :to="p.path"
                class="text-ink-secondary text-sm hover:text-blue-bright transition-colors"
              >
                {{ p.label }}
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Company -->
        <div>
          <h4 class="text-ink-primary text-xs font-semibold tracking-widest uppercase mb-4">公司</h4>
          <ul class="space-y-2">
            <li v-for="c in company" :key="c.path">
              <router-link
                :to="c.path"
                class="text-ink-secondary text-sm hover:text-blue-bright transition-colors"
              >
                {{ c.label }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <div class="divider mt-10 pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-ink-muted text-xs">
          © {{ new Date().getFullYear() }} AI智能终端. All rights reserved.
        </p>
        <p class="text-ink-muted text-xs">
          contact@ai-terminal.com
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const products = [
  { label: 'AI眼镜 VISION G1', path: '/products/ai-glasses' },
  { label: 'AI机器人 NEXUS R2', path: '/products/ai-robot' },
  { label: 'AI玩具 MOCHI A1', path: '/products/ai-toy' },
]

const company = [
  { label: '关于我们', path: '/about' },
  { label: '联系我们', path: '/contact' },
]
</script>
