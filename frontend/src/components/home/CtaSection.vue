<template>
  <section class="section bg-canvas relative overflow-hidden">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-0 left-1/3 w-48 h-48 bg-blue-base/5 rounded-full blur-3xl" />
      <div class="absolute bottom-0 right-1/3 w-48 h-48 bg-blue-base/5 rounded-full blur-3xl" />
    </div>

    <div class="relative max-w-3xl mx-auto text-center reveal">
      <p class="label-tag mb-6 inline-flex">Ready to Connect</p>
      <h2 class="text-3xl md:text-4xl font-bold text-ink-primary mb-4">
        准备好开始合作了吗？
      </h2>
      <p class="text-ink-secondary mb-10 text-lg max-w-xl mx-auto">
        无论是商务合作、渠道代理，还是产品体验预约，我们期待与您连接。
      </p>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <AppBtn variant="primary" size="lg" to="/contact">立即联系我们</AppBtn>
        <AppBtn variant="outline" size="lg" to="/#products">浏览产品</AppBtn>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import AppBtn from '@/components/common/AppBtn.vue'
</script>
