<template>
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
      scrolled ? 'bg-canvas/95 backdrop-blur-sm border-b border-line-base' : 'bg-transparent',
    ]"
  >
    <nav class="max-w-7xl mx-auto px-4 md:px-8 h-16 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2 group">
        <div class="w-8 h-8 rounded bg-gradient-blue flex items-center justify-center">
          <span class="text-canvas font-bold text-sm">AI</span>
        </div>
        <span class="font-semibold text-ink-primary group-hover:text-blue-bright transition-colors">
          智能终端
        </span>
      </router-link>

      <!-- Desktop Nav -->
      <ul class="hidden md:flex items-center gap-8">
        <li v-for="item in navItems" :key="item.path">
          <router-link
            :to="item.path"
            class="text-sm text-ink-secondary hover:text-blue-bright transition-colors"
            active-class="text-blue-bright"
          >
            {{ item.label }}
          </router-link>
        </li>
      </ul>

      <!-- CTA -->
      <AppBtn variant="outline" size="md" to="/contact" class="hidden md:inline-flex text-sm px-4 py-2">
        商务合作
      </AppBtn>

      <!-- Mobile Menu Toggle -->
      <button
        class="md:hidden text-ink-secondary hover:text-ink-primary p-2"
        @click="mobileOpen = !mobileOpen"
        aria-label="菜单"
      >
        <svg v-if="!mobileOpen" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </nav>

    <!-- Mobile Menu -->
    <div
      v-if="mobileOpen"
      class="md:hidden bg-canvas/98 border-b border-line-base px-4 py-4"
    >
      <ul class="flex flex-col gap-4">
        <li v-for="item in navItems" :key="item.path">
          <router-link
            :to="item.path"
            class="block text-sm text-ink-secondary hover:text-blue-bright transition-colors py-1"
            active-class="text-blue-bright"
            @click="mobileOpen = false"
          >
            {{ item.label }}
          </router-link>
        </li>
        <li>
          <AppBtn variant="outline" size="md" to="/contact" class="w-full justify-center text-sm py-2" @click="mobileOpen = false">
            商务合作
          </AppBtn>
        </li>
      </ul>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import AppBtn from './AppBtn.vue'

const scrolled = ref(false)
const mobileOpen = ref(false)

const navItems = [
  { label: '首页', path: '/' },
  { label: 'AI眼镜', path: '/products/ai-glasses' },
  { label: 'AI机器人', path: '/products/ai-robot' },
  { label: 'AI玩具', path: '/products/ai-toy' },
  { label: '关于我们', path: '/about' },
]

function handleScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', handleScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>
