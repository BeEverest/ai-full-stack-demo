<template>
  <div>
    <HeroSection />
    <ProductMatrix />
    <TechHighlights />
    <BrandStatement />
    <MediaBadges />
    <CtaSection />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import HeroSection from '@/components/home/HeroSection.vue'
import ProductMatrix from '@/components/home/ProductMatrix.vue'
import TechHighlights from '@/components/home/TechHighlights.vue'
import BrandStatement from '@/components/home/BrandStatement.vue'
import MediaBadges from '@/components/home/MediaBadges.vue'
import CtaSection from '@/components/home/CtaSection.vue'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useProductStore } from '@/stores/product'

useScrollAnimation()
const store = useProductStore()
onMounted(() => store.loadProducts())
</script>
