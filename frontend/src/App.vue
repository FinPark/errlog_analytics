<template>
  <q-app>
    <q-layout view="lHh Lpr lFf">
      <!-- Header -->
      <q-header class="ams-header">
        <q-toolbar class="ams-toolbar">
          <q-btn
            flat
            dense
            round
            icon="menu"
            aria-label="Menu"
            class="text-grey-8"
            @click="toggleLeftDrawer"
          />
          
          <!-- AMS Logo -->
          <img 
            src="/ams-logo.svg" 
            alt="AMS" 
            class="ams-logo q-ml-md q-mr-lg"
          />
          
          <q-separator vertical class="q-mr-lg" />
          
          <div class="column q-py-sm">
            <div class="text-h6 text-primary">Finken's Error-Log Analytics</div>
            <div class="text-caption text-grey-7">Powered by AMS ERP</div>
          </div>
          
          <q-space />
          
          <!-- Navigation Items -->
          <q-tabs 
            v-model="currentRoute"
            no-caps
            inline-label
            class="text-grey-8"
          >
            <q-tab 
              name="dashboard" 
              label="Dashboard" 
              icon="dashboard"
              @click="$router.push('/dashboard')"
            />
            <q-tab 
              name="upload" 
              label="Upload" 
              icon="upload"
              @click="$router.push('/upload')"
            />
          </q-tabs>
          
          <q-space />
          
          <!-- User Menu -->
          <q-btn 
            flat 
            round 
            icon="account_circle"
            class="text-grey-8"
          >
            <q-menu>
              <q-list style="min-width: 200px">
                <q-item clickable v-close-popup>
                  <q-item-section avatar>
                    <q-icon name="person" />
                  </q-item-section>
                  <q-item-section>Profile</q-item-section>
                </q-item>
                <q-item clickable v-close-popup>
                  <q-item-section avatar>
                    <q-icon name="settings" />
                  </q-item-section>
                  <q-item-section>Settings</q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable v-close-popup @click="toggleDarkMode">
                  <q-item-section avatar>
                    <q-icon :name="themeStore.isDark ? 'light_mode' : 'dark_mode'" />
                  </q-item-section>
                  <q-item-section>{{ themeStore.isDark ? 'Light Mode' : 'Dark Mode' }}</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </q-toolbar>
      </q-header>

      <!-- Left Drawer -->
      <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        bordered
        :class="themeStore.isDark ? 'bg-grey-9' : 'bg-grey-1'"
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
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import ThemeToggle from '@/components/ThemeToggle.vue'

const $q = useQuasar()
const route = useRoute()
const leftDrawerOpen = ref(false)
const themeStore = useThemeStore()

// Current route for tabs
const currentRoute = computed(() => route.name as string)

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

<style lang="scss">
// AMS Header Styles - Light Mode
.body--light .ams-header {
  background: #ffffff !important;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
  
  .ams-toolbar {
    min-height: 80px;
    padding: 0 24px;
    
    .ams-logo {
      height: 45px;
      width: auto;
      // Filter to convert white SVG to AMS blue in light mode
      filter: brightness(0) saturate(100%) invert(13%) sepia(94%) saturate(3496%) hue-rotate(213deg) brightness(91%) contrast(101%);
    }
    
    .q-tabs {
      .q-tab {
        color: #6c757d;
        
        &.q-tab--active {
          color: var(--q-primary);
        }
      }
    }
  }
}

// AMS Header Styles - Dark Mode
.body--dark .ams-header {
  background: #2a2a2a !important;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
  
  .ams-toolbar {
    min-height: 80px;
    padding: 0 24px;
    
    .ams-logo {
      height: 45px;
      width: auto;
      // Keep logo visible in dark mode
      filter: none;
    }
    
    .q-tabs {
      .q-tab {
        color: #e0e0e0;
        
        &.q-tab--active {
          color: var(--q-primary);
        }
      }
    }
    
    .q-btn {
      color: #e0e0e0;
      
      &:hover {
        color: var(--q-primary);
      }
    }
    
    .text-primary {
      color: var(--q-primary) !important;
    }
    
    .text-grey-7 {
      color: #b0b0b0 !important;
    }
    
    .text-grey-8 {
      color: #e0e0e0 !important;
    }
  }
}


// Left Drawer Styling - Light Mode
.body--light .q-drawer {
  background: #f8f9fa !important;
  
  .q-list {
    .q-item {
      margin: 4px 8px;
      border-radius: 8px;
      color: #495057;
      
      &:hover {
        background: rgba(0, 61, 122, 0.08);
      }
      
      &.q-router-link--active {
        background: rgba(0, 61, 122, 0.12);
        color: var(--q-primary);
      }
    }
  }
}

// Left Drawer Styling - Dark Mode
.body--dark .q-drawer {
  background: #2a2a2a !important;
  
  .q-list {
    .q-item {
      margin: 4px 8px;
      border-radius: 8px;
      color: #e0e0e0;
      
      &:hover {
        background: rgba(0, 168, 225, 0.15);
      }
      
      &.q-router-link--active {
        background: rgba(0, 168, 225, 0.2);
        color: var(--q-primary);
      }
      
      .q-icon {
        color: #e0e0e0;
      }
    }
  }
}

// Page Container - Light Mode
.body--light .q-page-container {
  background: #f5f5f5;
}

// Page Container - Dark Mode
.body--dark .q-page-container {
  background: #1a1a1a;
}
</style>