<template>
  <AppNav />
  <main>
    <RouterView />
  </main>
  <AppFooter />
</template>

<script setup lang="ts">
import AppNav from '@/components/common/AppNav.vue'
import AppFooter from '@/components/common/AppFooter.vue'
</script>
