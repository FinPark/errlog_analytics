<template>
  <q-btn
    :icon="themeStore.isDark ? 'light_mode' : 'dark_mode'"
    :color="themeStore.isDark ? 'yellow' : 'blue-grey'"
    round
    flat
    @click="themeStore.toggleTheme"
  >
    <q-tooltip>
      Switch to {{ themeStore.isDark ? 'Light' : 'Dark' }} Mode
    </q-tooltip>
  </q-btn>
</template>

<script setup lang="ts">
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
</script>