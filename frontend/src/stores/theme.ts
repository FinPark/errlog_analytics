import { defineStore } from 'pinia'
import { Dark } from 'quasar'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDark: false
  }),

  getters: {
    currentTheme: (state) => state.isDark ? 'dark' : 'light'
  },

  actions: {
    initTheme() {
      // Check localStorage for saved preference
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        this.isDark = savedTheme === 'dark'
      } else {
        // Check system preference
        this.isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      this.applyTheme()
    },

    toggleTheme() {
      this.isDark = !this.isDark
      this.applyTheme()
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light')
    },

    applyTheme() {
      Dark.set(this.isDark)
    }
  }
})