<template>
  <section class="section bg-surface">
    <div class="max-w-5xl mx-auto">
      <p class="text-center text-ink-muted text-2xs tracking-widest uppercase mb-10 reveal">
        受到行业媒体与机构的广泛关注
      </p>
      <div class="flex flex-wrap items-center justify-center gap-8 md:gap-14 reveal reveal-delay-1">
        <div
          v-for="media in mediaList"
          :key="media.name"
          class="text-ink-muted/40 hover:text-ink-secondary transition-colors duration-200 text-sm font-semibold tracking-wider uppercase"
        >
          {{ media.name }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const mediaList = [
  { name: '36氪' },
  { name: '极客公园' },
  { name: 'TechCrunch' },
  { name: '虎嗅网' },
  { name: 'The Verge' },
  { name: '钛媒体' },
]
</script>
