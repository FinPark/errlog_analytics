<template>
  <q-app>
    <q-layout view="lHh Lpr lFf">
      <!-- Header -->
      <q-header elevated class="bg-primary text-white">
        <q-toolbar>
          <q-btn
            flat
            dense
            round
            icon="menu"
            aria-label="Menu"
            @click="toggleLeftDrawer"
          />
          <q-toolbar-title>
            <q-icon name="analytics" class="q-mr-sm" />
            Error Log Analytics
          </q-toolbar-title>
          
          <q-space />
          
          <!-- Theme Toggle -->
          <q-btn
            flat
            round
            dense
            :icon="themeStore.isDark ? 'light_mode' : 'dark_mode'"
            @click="toggleDarkMode"
          >
            <q-tooltip>
              {{ themeStore.isDark ? 'Light Mode' : 'Dark Mode' }}
            </q-tooltip>
          </q-btn>
        </q-toolbar>
      </q-header>

      <!-- Left Drawer -->
      <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        bordered
        class="bg-grey-1"
      >
        <q-list>
          <q-item-label header>Navigation</q-item-label>
          
          <q-item
            clickable
            v-ripple
            :to="{ name: 'home' }"
            exact-active-class="text-primary"
          >
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>
            <q-item-section>Home</q-item-section>
          </q-item>
          
          <q-item
            clickable
            v-ripple
            :to="{ name: 'upload' }"
            exact-active-class="text-primary"
          >
            <q-item-section avatar>
              <q-icon name="upload" />
            </q-item-section>
            <q-item-section>Upload Logs</q-item-section>
          </q-item>
          
          <q-item
            clickable
            v-ripple
            :to="{ name: 'dashboard' }"
            exact-active-class="text-primary"
          >
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>
        </q-list>
      </q-drawer>

      <!-- Main Content -->
      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </q-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useThemeStore } from '@/stores/theme'
import ThemeToggle from '@/components/ThemeToggle.vue'

const $q = useQuasar()
const leftDrawerOpen = ref(false)
const themeStore = useThemeStore()

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function toggleDarkMode() {
  themeStore.toggleTheme()
}

onMounted(() => {
  themeStore.initTheme()
})
</script>