<template>
  <component
    :is="to ? RouterLink : 'button'"
    :to="to"
    :class="[
      variant === 'primary' ? 'btn-primary' : 'btn-outline',
      size === 'lg' ? 'lg' : '',
    ]"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
defineProps<{ variant?: 'primary' | 'outline'; size?: 'md' | 'lg'; to?: string }>()
</script>
